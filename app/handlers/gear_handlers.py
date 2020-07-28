import logging
from contextlib import suppress

from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageToDeleteNotFound

from ..database.base import User, Item
from ..handlers.user_handlers import user_inventory
from ..helpers.dev_text import gear_info_text
from ..helpers.keyboards import CRAFT_Kb, EQUIPMENT_Kb, IDLE_Kb, UNDRESS_Kb


async def gear_info_check(m: Message):
    try:
        gear = await Item.get(int(m.text[1:]))
        if gear:
            await m.answer(text=gear_info_text(gear))
        else:
            with suppress(MessageToDeleteNotFound):
                await m.delete()
            await m.answer('❗ Такого предмета не существует') 
    except ValueError:
        return
    


async def gear_equip(c: CallbackQuery, user: User):
    if c.data[6:] == 'back':
        with suppress(MessageToDeleteNotFound):
            await c.message.delete()
        await user_inventory(c.message, user)
    else:
        gear = await Item.get(int(c.data[6:]))
        if gear.id in user.inventory:
            if getattr(user, gear.item_class) is None:
                user.inventory.remove(gear.id)
                await user.update(inventory=user.inventory, defence=user.defence + gear.defence_boost,
                                max_defence=user.max_defence + gear.defence_boost, 
                                damage=user.damage + gear.attack_boost).apply()
                
                await user.update(weapon=gear.id).apply() if gear.item_class == 'weapon' else await user.update(armor=gear.id).apply()
                    
                await c.message.delete()
                await c.message.answer(text="❕ Вы надели экипировку", reply_markup=IDLE_Kb())
            else:
                await c.message.delete()
                await c.message.answer(text="❗ Сначала снимите экипировку", reply_markup=EQUIPMENT_Kb())
        else:
            await c.message.delete()
            await c.message.answer(text="❗ У вас нету такого предмета", reply_markup=IDLE_Kb())
    


async def gear_unequip(m: Message, user: User):
    if (user.weapon or user.armor) != None:
        eq = [user.weapon, user.armor]
        data = []
        for i in range(len(eq)):
            if eq[i] != None:
                gear = await Item.get(eq[i])
                data.extend([gear.name, gear.id])
            else:
                data.extend(['- Пусто -', 'empty'])
        await m.answer('❔ Выбери какую экипировку снимать:',
                       reply_markup=UNDRESS_Kb(data))
    else:
        await m.answer('❗ У тебя нету экипировки', reply_markup=IDLE_Kb())


async def gear_unequip_query(c: CallbackQuery, user: User):
    gear = await Item.get(int(c.data[8:]))
    # user.weapon => Common Sword (example)
    if gear:
        user.inventory.append(gear.id)
        await user.update(defence=user.defence - gear.defence_boost if user.defence - gear.defence_boost >= 0 else 0, 
                          max_defence=user.max_defence - gear.defence_boost,
                          damage=user.damage - gear.attack_boost, inventory=user.inventory).apply()
        await user.update(weapon=None).apply() if gear.item_class == 'weapon' else await user.update(armor=None).apply()

        with suppress(MessageToDeleteNotFound):
            await c.message.delete()
        await c.message.answer(f"❕ Вы сняли \"{gear.name}\"", reply_markup=IDLE_Kb())
    else:
        with suppress(MessageToDeleteNotFound):
            await c.message.delete()
        await c.message.answer('❗ У тебя нету экипировки', reply_markup=IDLE_Kb())


async def gear_craft(m: Message, user: User):
    raw = []
    if user.inventory:
        inv = dict((x, int(user.inventory.count(x) / 2)) for x in set(user.inventory) if user.inventory.count(x) != 1)
        if inv:
            for x, y in inv.items():
                raw_items = await Item.get(int(x))
                if raw_items:
                    for _ in range(y):
                        raw.append(raw_items)
            print(inv, '|', raw_items, '|', raw)
            await m.answer(text='🧳❕ Выберите какую пару предметов крафтить:', reply_markup=CRAFT_Kb(raw))
        else:
            await m.answer(text='❗ У вас нету подходящих предметов', reply_markup=IDLE_Kb())
    else:
        await m.answer(text='❗ Инвентарь пуст', reply_markup=IDLE_Kb())


async def gear_craft_query(c: CallbackQuery, user: User):
    curr_gear = await Item.get(int(c.data[6:]))
    if curr_gear:
        for _ in range(2):
            if curr_gear.id in user.inventory:
                user.inventory.remove(curr_gear.id)
            else:
                with suppress(MessageToDeleteNotFound):
                    await c.message.delete()
                await c.message.answer('❕ В вашем инвентаре больше нету такого предмета', reply_markup=IDLE_Kb())
                return

        craft_result = await Item.get(curr_gear.id + 1)
        if curr_gear.item_class == craft_result.item_class:
            user.inventory.append(craft_result.id)
            await user.update(inventory=user.inventory).apply()
            with suppress(MessageToDeleteNotFound):
                await c.message.delete()
            await c.message.answer(
                text=f"❕ Вы успешно скрафтили предмет:\n\n{gear_info_text(craft_result)}",
                reply_markup=IDLE_Kb())
        else:
            with suppress(MessageToDeleteNotFound):
                await c.message.delete()
            await c.message.answer('❗ Предметы уже максимального качества', reply_markup=IDLE_Kb())
    else:
        with suppress(MessageToDeleteNotFound):
            await c.message.delete()
        await c.message.answer('<b>Error:</b> Broken item (Свяжитесь с администрацией)', reply_markup=IDLE_Kb())
        raise NameError("Broken item")
