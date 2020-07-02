import logging
from contextlib import suppress

from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageToDeleteNotFound

from ..helpers.dev_text import gear_info_text, user_text
from ..helpers.keyboards import (EQUIP_Kb, EQUIPMENT_Kb, HEAL_CONFIRM_Kb,
                                 HEAL_PURCHASE_Kb, IDLE_Kb, INVENTORY_Kb,
                                 PROFILE_Kb, UPDATE_STATS_Kb)

from ..database.base import User, Item


async def user_profile(m: Message, user: User, clean=True):
    boost, equipment = [], []
    if user.weapon or user.armor:
        eq = [user.weapon, user.armor]
        for i in range(len(eq)):
            if eq[i]:
                gear = await Item.get(eq[i])
                if gear:
                    equipment.append(gear.name)
                    boost.extend([gear.attack_boost, gear.defence_boost])
            else:
                equipment.append(None)
                boost.extend([0, 0])
    else:
        boost = None
    
    await m.answer(text=user_text(user, m.from_user.first_name, boost, equipment),
                   reply_markup=PROFILE_Kb() if clean is True else IDLE_Kb())



async def user_inventory(m: Message, user: User):
    if user.inventory:
        formatted = []
        for x in user.inventory:
            raw_item = await Item.get(x)
            if raw_item:
                formatted.append(raw_item)
        await m.answer(text='🧳 Содержимое инвентаря:', reply_markup=INVENTORY_Kb(formatted))
    else:
        await m.answer(text='❗ Инвентарь пуст')
    pass


async def user_inventory_items(c: CallbackQuery):
    gear = await Item.get(c.data[4:])
    if gear:
        await c.message.edit_text(text=gear_info_text(gear), reply_markup=EQUIP_Kb(gear.id))
    else:
        with suppress(MessageToDeleteNotFound):
            await c.message.delete()
        await c.message.answer('<b>Error:</b> Broken item | Свяжитесь с администрацией')
        logging.error(f"Broken item \"{c.data[4:]}\", {c.from_user.id}")



async def user_equipment(m: Message):
    await m.answer('❕ Выберите действие:', reply_markup=EQUIPMENT_Kb())


async def user_heal(m: Message, user: dict):
    if user.heal_potions > 0:
        await m.answer(f"Вы уверены что хотите использовать <i>Лечебное зелье</i>?\n"
                       f"У вас осталось: <b>{user.heal_potions}</b>шт.", reply_markup=HEAL_CONFIRM_Kb())
    else:
        await m.answer('❗ У тебя не осталось лечебных зелий', reply_markup=HEAL_PURCHASE_Kb((user.lvl * 10) // 4))


async def user_heal_query(c: CallbackQuery, user: User):
    if user.heal_potions > 0:
        with suppress(MessageToDeleteNotFound):
            await c.message.delete()
        await user.update(health=user.max_health, defence=user.max_defence, heal_potions=user.heal_potions-1).apply()
        await user_profile(c.message, user, False)
    else:
        await c.message.answer('❗ У тебя не осталось лечебных зелий',
                               reply_markup=HEAL_PURCHASE_Kb((user.lvl * 10) // 4))



async def user_stats_increase(m: Message, user: User):
    await m.delete()
    if user.level_points > 0:
        await m.answer(text="Какую характеристику повышать?", reply_markup=UPDATE_STATS_Kb())
    else:
        await m.answer('❗ У тебя нету очков повышения!')


async def user_stats_increase_query(c: CallbackQuery, user: User):
    if user.level_points > 0:
        if c.data[13:] == 'damage':
            await user.update(attack=user.damage+1, level_points=user.level_points-1).apply()
            await c.answer('❕ Урон увеличен.', show_alert=True)
        elif c.data[13:] == 'health':
            await user.update(attack=user.max_health+1, level_points=user.level_points-1).apply()
            await c.answer('❕ Здоровье увеличено', show_alert=True)
        elif c.data[13:] == 'defence':
            await user.update(attack=user.max_defence+1, level_points=user.level_points-1).apply()
            await c.answer('❕ Защита увеличена', show_alert=True)
    else:
        await c.message.edit_text(text='❗ Ты использовал все очки повышения')
