import logging
from contextlib import suppress
from random import choice, randint, uniform

from aiogram.dispatcher import FSMContext
from aiogram.types import (CallbackQuery, KeyboardButton, Message,
                           ReplyKeyboardMarkup)
from aiogram.types.chat import ChatActions
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageCantBeDeleted, MessageCantBeEdited
from sqlalchemy import and_

from app.__main__ import bot

from ..database.base import Item, User, Ability
from ..helpers.dev_text import lvl_up_text, meet_enemy_text, rankup_text
from ..helpers.keyboards import (ATTACK_Kb, CONFIRM_BATTLE_Kb, DEFENCE_Kb,
                                 IDLE_Kb, PROFILE_Kb, PVE_LEAVE_Kb,
                                 STATS_INC_Kb, BATTLE_MENU_Kb, ABILITIES_Kb)
from ..helpers.scenario import MOB_NAMES
from ..models import Enemy, AbilityMethods
from ..utils.game_logic import (battle_attack, battle_defence, exam_choose,
                                get_xp, item_drop, power, round_down,
                                set_difficulty, enemy_calc)
from ..utils.states import MainStates


async def pve_rankup(m: Message, state: FSMContext, user: User):
    if user.health > 0:
        await MainStates.battle.set()
        async with state.proxy() as data:
            trash = await m.answer('⏳ <i>Башня готовит вам экзаменатора..</i>',
                                reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('~')))
            await ChatActions().typing(sleep=randint(1, 4))
            
            with suppress(MessageCantBeDeleted):
                await trash.delete()
            data['enemy'] = exam_choose(user)
            await m.reply('=============================', reply_markup=PVE_LEAVE_Kb())
            
            if data['enemy'] != '❕ Максимальный ранг!':
                diff = set_difficulty(data['enemy'].power, power(user))
                data['msg'] = await m.answer(text=rankup_text(data['enemy'], user, diff), reply_markup=CONFIRM_BATTLE_Kb())
            else:
                await state.reset_data()
                await state.reset_state()
                await m.answer(text=data['enemy'], reply_markup=IDLE_Kb())
    else:
        await m.answer(text="❗ Ты мёртв...")


async def pve_battle(m: Message, state: FSMContext, user: User):
    if user.health > 0:
        await MainStates.battle.set()
        async with state.proxy() as data:
            trash = await m.answer('⏳ <i>Башня ищет вам противника..</i>',
                                   reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('~')))
            await ChatActions().typing(sleep=randint(1, 4))
            raw_enemy = enemy_calc(user.damage, user.health, user.defence, user.lvl)

            with suppress(MessageCantBeDeleted):
                await trash.delete()
            data['enemy'] = Enemy(name=choice(MOB_NAMES), damage=raw_enemy[0][0], health=raw_enemy[0][1], defence=raw_enemy[0][2], 
                                  drop_chance=randint(1, 15), bonus=raw_enemy[1])
            await m.reply('=============================', reply_markup=PVE_LEAVE_Kb())
            data['msg'] = await m.answer(text=meet_enemy_text(data['enemy'], set_difficulty(power(data['enemy']), power(user))),
                                         reply_markup=CONFIRM_BATTLE_Kb())
    else:
        await m.answer(text="❗ Ты мёртв...")


async def pve_confirmed(c: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await data['msg'].edit_text('⏳ <i>Башня готовит поле боя..</i>')
        await ChatActions().typing(sleep=randint(1, 4))

        await data['msg'].edit_text(text="⚔️ Выбери действие:", reply_markup=BATTLE_MENU_Kb("🛡 Защищаться", "defence_menu", False))

 
async def pve_attack_menu(c: CallbackQuery, state: FSMContext, user: User):
    async with state.proxy() as data:
        if c.message.message_id == data['msg'].message_id:
            await data['msg'].edit_text(text='🗡 Выберите место которое хотите атаковать:', reply_markup=ATTACK_Kb())
        else:
            await c.message.edit_text("❗ Данный бой потерял актуальность")


async def pve_defence_menu(c: CallbackQuery, state: FSMContext, user: User):
    async with state.proxy() as data:
        if c.message.message_id == data['msg'].message_id:
            await data['msg'].edit_text(text='🗡 Выберите место которое хотите защищать:', reply_markup=DEFENCE_Kb())
        else:
            await c.message.edit_text("❗ Данный бой потерял актуальность")


# 'abilities_menu_'
async def pve_abilities(c: CallbackQuery, state: FSMContext, user: User, step=None):
    async with state.proxy() as data:
        if c.message.message_id == data['msg'].message_id:
            if user.abilities:
                mode = c.data[15:18] if not step else step
                abilities = [await Ability.get(x) for x in user.abilities if await Ability.get(x)]
                await data['msg'].edit_text(text='🎴 Доступные способности:', 
                                            reply_markup=ABILITIES_Kb(abilities=abilities, battle=True, attack=True if mode == 'atk' else False))
            else:
                await c.answer(text='❗ У вас нету способностей', show_alert=True)
        else:
            await c.message.edit_text("❗ Данный бой потерял актуальность")


# 'battle_ability_'
async def pve_abilities_query(c: CallbackQuery, user: User, state: FSMContext):
    if (c.data[:23] == 'battle_ability_atk_use_' or c.data[:23] == 'battle_ability_def_use_'):
        ability = await Ability.get(int(c.data[23:]))
        method = getattr(AbilityMethods(), ability.func)
        await method(c, user, ability, state)
    elif (c.data == 'battle_ability_atk_back' or c.data == 'battle_ability_def_back'):
        await pve_abilities(c, state, user, c.data[15:18])
        

async def pve_attack(c: CallbackQuery, state: FSMContext, user: User):
    async with state.proxy() as data:
        data['results'] = data['results'] if data.get('results') else []
        if c.message.message_id == data['msg'].message_id:
            pre_health, pre_defence = data['enemy'].health, data['enemy'].defence  # stats before pve'ing
            # user's dealing damage to mob:
            data['enemy'].health, data['enemy'].defence = await battle_attack(0, randint(0, 3), user, data['enemy'], call=c)
            data['results'].append(f"🗡 \"{data['enemy'].name}\" - ♥:{data['enemy'].health}(-{(pre_health-data['enemy'].health) if (pre_health-data['enemy'].health)!=0 else 'miss'}) | "
                                   f"🛡:{data['enemy'].defence}(-{(pre_defence-data['enemy'].defence) if (pre_defence-data['enemy'].defence)!=0 else 'miss'})")
            await c.answer(text=data['results'][-1], show_alert=True)
            if data['enemy'].health > 0:  # if user still alive:
                # next step:
                await data['msg'].edit_text(text="⚔️ Выбери действие:", reply_markup=BATTLE_MENU_Kb("🛡 Защищаться", "defence_menu", False))
            else: # if dead:
                try:
                    if hasattr(data['enemy'], 'bonus'):  # if not examinator (examinators have no bonuses):
                        with suppress(MessageCantBeEdited):
                            await data['msg'].edit_text('\n'.join(data['results']))

                        await c.message.answer('=============================')
                        await c.answer("☠️ Враг умер")
                        total_xp = get_xp(user.lvl)
                        try:
                            if user.xp + data['enemy'].bonus >= total_xp:
                                lvl_increase = (user.xp + data['enemy'].bonus) // total_xp
                                user.level_points += 3 * lvl_increase
                                await user.update(level_points=user.level_points, 
                                                  xp=user.xp+data['enemy'].bonus, 
                                                  lvl=user.lvl+lvl_increase).apply()
                                # encouraging user:
                                await c.message.answer(
                                    text=f"🎊 Вы получили +{data['enemy'].bonus}<i>XP</i>, в связи с чем ваш уровень повышен!\n"
                                         f"<i>Вам засчитано (3) очки повышения.</i>", reply_markup=PROFILE_Kb())
                            else:
                                # encouraging user:
                                await user.update(health=user.health, defence=user.defence, xp=user.xp+data['enemy'].bonus).apply()
                                await c.message.answer(text=f"✨ Вы получили +{data['enemy'].bonus} <i>XP</i>!", reply_markup=IDLE_Kb())
                        finally:
                            await user.update(balance=user.balance + round(data['enemy'].bonus / 2)).apply()
                            # encouraging user:
                            await c.message.answer(text=f"💰 Вы получили +{round(data['enemy'].bonus / 2)} <i>мoнет</i>!")
                            if item_drop(data['enemy'].drop_chance) is True:
                                drop_list = await Item.query.where(and_(Item.rank == user.rank, Item.quality == 'Common')).gino.all()
                                if drop_list:
                                    dropped_item = choice(drop_list)
                                    user.inventory.append(dropped_item.id)
                                    await user.update(inventory=user.inventory).apply()
                                    # encouraging user:
                                    await c.message.answer(f"❗ Вам выпал предмет: \n\"{dropped_item.name}\".\n"
                                                             f"<i>Предмет помещён в ваш инвентарь</i>")
                                else:
                                    c.message.answer('❗ Ёпрст, ваш ранг выше чем ранг существующего оружия.')
                    else:
                        with suppress(MessageCantBeEdited):
                            await data['msg'].edit_text('\n'.join(data['results']))
                        await c.message.answer('=============================')
                        await user.update(rank=data['enemy'].rank, level_points=user.level_points+5).apply()
                        # encouraging user:
                        await c.message.answer(
                            f"🎊 Вы победили экзаменатора! Поздравляем, теперь ваш ранг - {data['enemy'].rank}. "
                            f"<i>Вам засчитано (5) очков повышения.</i>", reply_markup=STATS_INC_Kb())
                finally:
                    await state.reset_state()
                    await state.reset_data()
        else:
            await c.message.edit_text("❗ Данный бой потерял актуальность")


async def pve_defence(c: CallbackQuery, state: FSMContext, user: User):
    async with state.proxy() as data:
        data['results'] = data['results'] if data.get('results') else []
        if c.message.message_id == data['msg'].message_id:
            pre_health, pre_defence = user.health, user.defence  # stats before pve'ing
            # mob's dealing damage to user:
            user.health, user.defence = await battle_defence(0, randint(0, 3), user, data['enemy'], call=c)
            data['results'].append(f"⚔️ \"{user.username}\" - ♥:{user.health}(-{(pre_health-user.health) if (pre_health-user.health)!=0 else 'miss'}) | "
                                   f"🛡:{user.defence}(-{(pre_defence-user.defence) if (pre_defence-user.defence)!=0 else 'miss'})")
            await c.answer(text=data['results'][-1], show_alert=True)                    
            if user.health > 0: # if user still alive:
                await user.update(health=user.health, defence=user.defence).apply() 
                # next step:
                await data['msg'].edit_text(text="⚔️ Выбери действие:", reply_markup=BATTLE_MENU_Kb("🗡 Атаковать", "attack_menu", True))
            else: # if dead:
                try:
                    if hasattr(data['enemy'], 'bonus'):  # if not examinator (examinators have no bonuses):
                        with suppress(MessageCantBeEdited):
                            await data['msg'].edit_text('\n'.join(data['results']))
                        await c.message.answer('=============================')
                        await user.update(health=1, defence=0, xp=user.xp - data['enemy'].bonus if user.xp - data['enemy'].bonus > 0 else -1, 
                                        balance=(user.balance - data['enemy'].bonus // 2 if user.balance - data['enemy'].bonus // 2 > 0 else -1) if user.lvl>2 else user.balance).apply()
                        # encouraging user:
                        await c.message.answer(text="☠️ Ты проиграл, потерял опыт и деньги, а ещё у тебя 1 хп! Не сдавайся!", reply_markup=IDLE_Kb())
                        logging.info(f"{user.username} умер")
                    else:
                        with suppress(MessageCantBeEdited):
                            await data['msg'].edit_text('\n'.join(data['results']))
                        await c.message.answer('=============================')
                        await user.update(health=1, defence=0).apply()
                        # encouraging user:
                        await c.message.answer(text="❗ Экзамен провален!", reply_markup=IDLE_Kb())
                finally:
                    await state.reset_state()
                    await state.reset_data()
        else:
            await c.message.edit_text("❗ Данный бой потерял актуальность")


async def pve_leave_battle(m: Message, state: FSMContext, user: User):
    async with state.proxy() as data:
        if data.get('msg'):
            try:
                with suppress(MessageToDeleteNotFound):
                    await m.delete()
                    await data['msg'].delete()
                await m.answer('============================')
                await user.update(xp=user.xp - data['enemy'].bonus // 2 if user.xp - data['enemy'].bonus // 2 > 0 else -1).apply()
                await m.answer(
                    text=f"☠️ <i>Башня зарегистрировала твоё поражение\n Опыт понижен на {data['enemy'].bonus // 2}XP</i>", reply_markup=IDLE_Kb())
            except KeyError:
                return
            finally:
                await state.reset_state()
                await state.reset_data()
