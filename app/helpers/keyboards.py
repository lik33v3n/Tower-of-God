from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# MAIN KEYBOARDS:
def IDLE_Kb():
    main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    main_kb.add(
        KeyboardButton(text='👤 Профиль')).add(
        KeyboardButton(text='💼 Инвентарь')).add(
        KeyboardButton(text='⚔️ Бой')).add(
        KeyboardButton(text='💉 Лечение'))
    return main_kb


def PROFILE_Kb():
    pfl_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    pfl_kb.row(KeyboardButton(text='🥋 Экипировка'),
               KeyboardButton(text='⚖️ Повышение характеристик'))
    pfl_kb.row(KeyboardButton(text='📯 Повышение ранга'),
               KeyboardButton(text='🔙 Назад'))
    return pfl_kb


def EQUIPMENT_Kb():
    reply_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reply_kb.add(
        KeyboardButton(text='📤 Снять экипировку')).add(
        KeyboardButton(text='⚒ Крафт')).add(
        KeyboardButton(text='🛒 Торговая площадка')).add(
        KeyboardButton(text='🔙 Назад'))
    return reply_kb


def HEALING_Kb():
    reply_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reply_kb.add(
        KeyboardButton(text='💊 Лазарет')).add(
        KeyboardButton(text='🧪 Лечебные зелья')).add(
        KeyboardButton(text='🔙 Назад'))
    return reply_kb


def STATS_INC_Kb():
    kb = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton(text="⚖️ Повышение характеристик"), KeyboardButton(text="🔙 Назад"))
    return kb


def SHOP_Kb(queue, page):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.row(InlineKeyboardMarkup(text='👤 К моим лотам', callback_data='shop_my'), 
           InlineKeyboardMarkup(text='🔄 Обновить', callback_data='shop_refresh'))
    if queue: 
        kb.add(*[InlineKeyboardButton(text=f'{item.item} - 💰{item.price}', callback_data=f'shop_get_{item.id}') for item in queue[page*5:page*5+5]])
    else:
        kb.add(InlineKeyboardMarkup(text='-', callback_data='empty'))
    kb.row(InlineKeyboardMarkup(text='◀️', callback_data='shop_back'), 
           InlineKeyboardMarkup(text=f'{page+1}/{len(queue)//5+1 if len(queue)%5>0 else len(queue)//5}', callback_data='empty'), 
           InlineKeyboardMarkup(text='▶️', callback_data='shop_forward'))
    kb.add(InlineKeyboardButton(text="🔚 Закрыть", callback_data='back'))
    return kb


def SHOP_MY_Kb(queue, page):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.row(InlineKeyboardMarkup(text='🌐 К всем лотам', callback_data='shop_refresh'),
           InlineKeyboardMarkup(text='🔄 Обновить', callback_data='shop_refresh_my'))
    kb.add(*[InlineKeyboardButton(text=f'{item.item} - 💰{item.price}', callback_data=f'shop_get_my_{item.id}') for item in queue[page*5:page*5+5]])
    kb.row(InlineKeyboardMarkup(text='◀️', callback_data='shop_my_back'), 
           InlineKeyboardMarkup(text=f'{page+1}/{len(queue)//5+1 if len(queue)%5>0 else len(queue)//5}', callback_data='empty'), 
           InlineKeyboardMarkup(text='▶️', callback_data='shop_my_forward')).add(
           InlineKeyboardButton(text="🔚 Закрыть", callback_data='back')) 
    return kb


def SHOP_MY_LOT_Kb(lot):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text='🚫 Отменить лот', callback_data=f'shop_lot_delete_{lot}')).add(
           InlineKeyboardButton(text='🔙 Назад', callback_data='shop_refresh_my'))
    return kb


def SHOP_LOT_Kb(lot):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text='💸 Приобрести предмет', callback_data=f'shop_lot_buy_{lot}')).add(
           InlineKeyboardButton(text='🔙 Назад', callback_data='shop_refresh'))
    return kb


def ATTACK_Kb():
    attack_keyboard = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text="Голова", callback_data="attack_mob")
    btn2 = InlineKeyboardButton(text="Грудь", callback_data="attack_mob")
    btn3 = InlineKeyboardButton(text="Живот", callback_data="attack_mob")
    btn4 = InlineKeyboardButton(text="Ноги", callback_data="attack_mob")
    attack_keyboard.add(btn1, btn2, btn3, btn4)
    return attack_keyboard


def BATTLE_MENU_Kb(first_text, first_callback):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text=first_text, callback_data=first_callback)).add(
           InlineKeyboardButton(text="⚗️ Бафы", callback_data="buffs_menu")).add(
           InlineKeyboardButton(text="🎲 Способности", callback_data="abilities_menu"))
    return kb


def DEFENCE_Kb():
    defence_keyboard = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text="Голова", callback_data="defence_mob")
    btn2 = InlineKeyboardButton(text="Грудь", callback_data="defence_mob")
    btn3 = InlineKeyboardButton(text="Живот", callback_data="defence_mob")
    btn4 = InlineKeyboardButton(text="Ноги", callback_data="defence_mob")
    defence_keyboard.add(btn1, btn2, btn3, btn4)
    return defence_keyboard


def CONFIRM_BATTLE_Kb():
    kb = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text="⚔️ В бой!", callback_data="battle_state")
    button2 = InlineKeyboardButton(text="✖️ Убежать", callback_data="back")
    kb.add(button1, button2)
    return kb


def PVE_LEAVE_Kb():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('⛔️ Сдаться'))


def INVENTORY_ITEM_Kb(item_id):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text='📥 Надеть предмет', callback_data=f"equip_{item_id}"),
           InlineKeyboardButton(text='💸 Продать предмет', callback_data=f'sell_{item_id}'),
           InlineKeyboardButton(text='🔙 Назад', callback_data=f"equip_back"))
    return kb


def UNDRESS_Kb(data):
    kb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text=f"{data[0]}", callback_data=f'unequip_{data[1]}')
    btn2 = InlineKeyboardButton(text=f"{data[2]}", callback_data=f'unequip_{data[3]}')
    btn3 = InlineKeyboardButton(text="🔙 Назад", callback_data='back')
    kb.add(btn1, btn2, btn3)
    return kb


def UPDATE_STATS_Kb():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        *[InlineKeyboardButton(x, callback_data=f'update_level_{y}') for x, y in
          {'🗡 Урон +1': 'damage', '♥ Здоровье +1': 'health', '🛡 Защита +1': 'defence'}.items()]).add(
        InlineKeyboardButton(text="🔚 Закрыть", callback_data='back'))
    return kb


def HEAL_CONFIRM_Kb():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text="💉 Да", callback_data="use_heal_potion"))
    kb.add(InlineKeyboardButton(text="🔚 Закрыть", callback_data="back"))
    return kb


def HEAL_PURCHASE_Kb(minus):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text=f"Приобрести -{minus} монет", callback_data="buy_heal_potion"))
    kb.add(InlineKeyboardButton(text="🔚 Закрыть", callback_data="back"))
    return kb


def INVENTORY_Kb(inv):
    kb = InlineKeyboardMarkup(row_width=1)
    for i in range(len(inv)):
        kb.add(InlineKeyboardButton(text=inv[i].name, callback_data=f"inv_{inv[i].id}"))
    kb.add(InlineKeyboardButton(text="🔚 Закрыть", callback_data="back"))
    return kb


def CRAFT_Kb(inv):
    kb = InlineKeyboardMarkup(row_width=1)
    for i in range(len(inv)):
        kb.add(InlineKeyboardButton(text=f"x2 {inv[i].name}", callback_data=f"craft_{inv[i].id}"))
    kb.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))
    return kb


def HELP_Kb():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(*[InlineKeyboardButton(x, callback_data=f"help_menu_{y}") for x, y in
           {'Обучение (рекомендуется)': 'train', 'Описание игрового бота': 'desc', 'Функционал бота': 'func'}.items()])
    kb.row(InlineKeyboardButton(text='🔈 Прочее..', callback_data='help_menu_other'),
           InlineKeyboardButton(text='🔚 Закрыть', callback_data='back'))
    return kb


def FUNC_LIST_Kb():
    kb = InlineKeyboardMarkup(row_width=2)
    commands = ("👤 Профиль", "⚔️ Бой",
                "💉 Исцеление", "📯 Повышение ранга", "💼 Инвентарь", "📤 Снять экипировку", "🥋 Экипировка",
                "⚖️ Повышение характеристик", "⚒ Крафт", "🔈 Помощь", "🛒 Магазин")
    kb.add(*[InlineKeyboardButton(name, callback_data=f"help_{name}") for name in commands]).insert(
        InlineKeyboardButton(text="🔙 Назад", callback_data="help_back"))
    return kb


# def ADMIN_GET_Kb(matches):
#     kb = InlineKeyboardMarkup(row_width=1)
#     for i in range(len(matches)):
#         kb.insert(
#             InlineKeyboardButton(text=matches[i].username, callback_data=f"get_{matches[i].telegram_id}"))
#     return kb


def CONFIRM_Kb(text: tuple, callback: str, row_width: int = 2):
    kb = InlineKeyboardMarkup(row_width=row_width)
    kb.row(InlineKeyboardButton(text=text[0], callback_data=callback), 
           InlineKeyboardButton(text=text[1], callback_data='back'))
    return kb


def HEALING_STATE_Kb():
    reply_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    reply_kb.add(*[
        KeyboardButton(text='❔ Информация'),
        KeyboardButton(text='🔚 Покинуть лазарет')])
    return reply_kb