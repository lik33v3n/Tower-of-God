import logging
from contextlib import suppress
from random import choice, randint, uniform

from aiogram.dispatcher import FSMContext
from aiogram.types import (CallbackQuery, KeyboardButton, Message,
                           ReplyKeyboardMarkup)
from aiogram.types.chat import ChatActions
from aiogram.utils.exceptions import MessageToDeleteNotFound

from app.__main__ import bot

from ..database.base import Item, User
from ..helpers.dev_text import lvl_up_text, meet_enemy_text, rankup_text
from ..helpers.keyboards import (ATTACK_Kb, CONFIRM_BATTLE_Kb, DEFENCE_Kb,
                                 IDLE_Kb, PROFILE_Kb, PVE_LEAVE_Kb,
                                 STATS_INC_Kb)
from ..helpers.scenario import MOB_NAMES
from ..models.enemies import Enemy
from ..utils.game_logic import (battle_attack, battle_defence, exam_choose,
                                get_xp, item_drop, power, round_down,
                                set_difficulty)
from ..utils.states import MainStates


async def pve_rankup(m: Message, state: FSMContext, user: User):
    if user.health > 0:
        await MainStates.battle.set()
        await m.reply('⏳ <i>Башня готовит вам экзаменатора..</i>',
                      reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('~')))
        await ChatActions().typing(sleep=randint(1, 5))
        async with state.proxy() as data:
            data['enemy'] = exam_choose(user)
            if data['enemy'] != '❕ Максимальный ранг!':
                diff = set_difficulty(data['enemy'].power, power(user))
                await m.answer(text=rankup_text(data['enemy'], user, diff), reply_markup=CONFIRM_BATTLE_Kb())
            else:
                await m.answer(text=data['enemy'], reply_markup=IDLE_Kb())
    else:
        await m.answer(text="❗ Ты мёртв...")


async def pve_battle(m: Message, state: FSMContext, user: User):
    if user.health > 0:
        await m.reply('⏳ <i>Башня ищет вам противника..</i>',
                      reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('~')))
        await ChatActions().typing(sleep=randint(1, 5))
        multiplier = round_down(uniform(0.2, 1.2), 1)
        async with state.proxy() as data:
            enemy_power = (int(user.max_health * multiplier) + int(user.max_defence * multiplier)) * int(user.damage * multiplier)
            var = enemy_power / power(user)            
            enemy = Enemy(name=choice(MOB_NAMES), damage=int(user.damage * multiplier), 
                          health=int(user.max_health * multiplier), defence=int(user.max_defence * multiplier), 
                          drop_chance=randint(1, 15), bonus=int((enemy_power / user.lvl) * var))
            data['enemy'] = enemy
            print(multiplier, var)
            try:
                await m.answer(text=meet_enemy_text(data['enemy'], set_difficulty(power(data['enemy']), power(user))),
                               reply_markup=CONFIRM_BATTLE_Kb())
            except TypeError:
                await state.reset_state()
                await state.set_data({'enemy': {}})
                await m.answer(f'NO SUCH RANK | Свяжитесь с администрацией', reply_markup=IDLE_Kb())
    else:
        await m.answer(text="❗ Ты мёртв...")


async def pve_confirmed(c: CallbackQuery, state: FSMContext):
    with suppress(MessageToDeleteNotFound):
        await c.message.delete()
    await MainStates.battle.set()
    await c.message.answer('⏳ <i>Башня готовит поле боя..</i>', reply_markup=PVE_LEAVE_Kb())
    await ChatActions().typing(sleep=randint(1, 5))
    bot_msg = await c.message.answer(text="❕ Выбери место защиты:", reply_markup=DEFENCE_Kb())
    await state.update_data({'bot_message_id': bot_msg.message_id})


async def pve_attack(c: CallbackQuery, state: FSMContext, user: User):
    with suppress(MessageToDeleteNotFound):
        await c.message.delete()
    async with state.proxy() as data:
        enemy = data['enemy']
    if enemy != {}:
        enemy.health, enemy.defence = await battle_attack(0, randint(0, 3), user, enemy, call=c)
        await c.message.answer(text=f"🗡 \"{enemy.name}\" <b>(♥:{enemy.health} | 🛡:{enemy.defence})</b>")
        if enemy.health > 0:
            bot_msg = await c.message.answer(text="❕ Выбери место защиты:", reply_markup=DEFENCE_Kb())
            await state.update_data({'bot_message_id': bot_msg.message_id})
            await state.update_data({'enemy': enemy})
        else:
            try:
                if hasattr(enemy, 'bonus'):
                    await c.answer("☠️ Враг умер")
                    total_xp = get_xp(user.lvl)
                    try:
                        if user.xp + enemy.bonus >= total_xp:
                            lvl_increase = (user.xp + enemy.bonus) // total_xp
                            user.level_points += 3 * lvl_increase
                            await user.update(level_points=user.level_points, 
                                              xp=user.xp+enemy.bonus, 
                                              lvl=user.lvl+lvl_increase).apply()
                            # next stage:
                            if (user.lvl + lvl_increase) // 3 > user.stage - 1:
                                await user.update(stage=user.stage+1).apply()
                                if 15 <= user.stage + 1 <= 1000000:
                                    await user.update(level_points=user.level_points+3).apply()
                                    await c.message.answer(text=lvl_up_text(enemy.bonus, 6),
                                                           reply_markup=PROFILE_Kb())
                                else:
                                    await c.message.answer(text=lvl_up_text(enemy.bonus, 3),
                                                           reply_markup=PROFILE_Kb())
                            else:
                                await c.message.answer(
                                    text=f"🎊 Вы получили +{enemy.bonus}<i>XP</i>, и ваш уровень повышен!\n"
                                         f"<i>Вам засчитано (3) очки повышения.</i>", reply_markup=PROFILE_Kb())
                        else:
                            await user.update(health=user.health, defence=user.defence, xp=user.xp+enemy.bonus).apply()
                            await c.message.answer(text=f"✨ Вы получили +{enemy.bonus} <i>XP</i>!",
                                                   reply_markup=IDLE_Kb())
                    finally:
                        await user.update(balance=user.balance + enemy.bonus // 2).apply()
                        await c.message.answer(text=f"💰 Вы получили +{enemy.bonus // 2} <i>мoнет</i>!")
                        if item_drop(enemy.drop_chance) is True:
                            drop_list = await Item.query.where(Item.rank == user.rank, Item.quality == 'Common').gino.all()
                            if drop_list:
                                dropped_item = choice(drop_list)
                                await user.update(inventory=user.inventory.append(dropped_item.id)).apply()
                                await c.message.answer(f"❗ Вам выпал предмет: \"{dropped_item.name}\".\n"
                                                       f"<i>Предмет помещён в ваш инвентарь</i>")
                            else:
                                print('NO SUCH ITEMS ON THIS RANK')
                else:
                    await user.update(rank=enemy.rank, level_points=user.level_points+10).apply()
                    await c.message.answer(
                        f"🎊 Вы победили экзаменатора! Поздравляем, теперь ваш ранг - {enemy.rank}. "
                        f"<i>Вам засчитано (10) очков повышения.</i>", reply_markup=STATS_INC_Kb())
            finally:
                await state.reset_state()
                await state.set_data({'enemy': {}})
    else:
        await state.reset_state()
        await c.message.answer("❗ Данный бой потерял актуальность", reply_markup=IDLE_Kb())


async def pve_defence(c: CallbackQuery, state: FSMContext, user: User):
    with suppress(MessageToDeleteNotFound):
        await c.message.delete()
    async with state.proxy() as data:
        enemy = data['enemy']
    if enemy != {}:
        user.health, user.defence = await battle_defence(0, randint(0, 3), user, enemy, call=c)
        await c.message.answer(text=f"🛡 {c.from_user.first_name} <b>(♥:{user.health} | 🛡:{user.defence})</b>")
        if user.health > 0:
            await user.update(health=user.health, defence=user.defence).apply()
            bot_msg = await c.message.answer(text="❕ Выбери место атаки:", reply_markup=ATTACK_Kb())
            await state.update_data({'bot_message_id': bot_msg.message_id})
        else:
            try:
                if hasattr(enemy, 'bonus'):
                    await user.update(health=1, defence=0, xp=user.xp - enemy.bonus if user.xp - enemy.bonus > 0 else -1, 
                                      balance=user.balance - enemy.bonus // 2 if user.balance - enemy.bonus // 2 > 0 else -1).apply()
                    await c.message.answer(
                        text="☠️ Ты проиграл, потерял опыт и деньги, а ещё у тебя 1 хп! Не сдавайся!",
                        reply_markup=IDLE_Kb())
                    logging.info(f"{c.from_user.first_name} умер")
                else:
                    await user.update(health=1, defence=0).apply()
                    await c.message.answer(text="❗ Экзамен провален!", reply_markup=IDLE_Kb())
                    logging.info(f"{c.from_user.first_name} провалил экзамен")
            finally:
                await state.reset_state()
                await state.set_data({'enemy': {}})
    else:
        await state.reset_state()
        await c.message.answer("❗ Данный бой потерял актуальность", reply_markup=IDLE_Kb())


async def pve_leave_battle(m: Message, state: FSMContext, user: User):
    async with state.proxy() as data:
        enemy = data['enemy']
        try:
            with suppress(MessageToDeleteNotFound):
                await bot.delete_message(chat_id=m.chat.id, message_id=data['bot_message_id'])
        except KeyError:
            return
    try:
        await user.update(xp=user.xp - enemy.bonus // 2 if user.xp - enemy.bonus // 2 > 0 else -1).apply()
        await m.answer(
            text=f"☠️ <i>Башня зарегистрировала твоё поражение\n Опыт понижен на {enemy.bonus // 2}XP</i>",
            reply_markup=IDLE_Kb())
        logging.info(f"{m.from_user.first_name} сдался")
    finally:
        await state.reset_state()
        await state.set_data({'enemy': {}})
