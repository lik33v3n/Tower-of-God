from aiogram import types


# MAIN KEYBOARDS:
def IDLE_Kb():
    main_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_kb.add(
        types.KeyboardButton(text='👤 Профиль')).add(
        types.KeyboardButton(text='💼 Инвентарь')).add(
        types.KeyboardButton(text='⚔️ Бой')).add(
        types.KeyboardButton(text='💉 Лечение'))
    return main_kb


def PROFILE_Kb():
    pfl_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    pfl_kb.row(types.KeyboardButton(text='🥋 Экипировка'),
               types.KeyboardButton(text='⚖️ Повышение характеристик'))
    pfl_kb.row(types.KeyboardButton(text='📯 Повышение ранга'),
               types.KeyboardButton(text='🔙 Назад'))
    return pfl_kb


def EQUIPMENT_Kb():
    reply_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reply_kb.add(
        types.KeyboardButton(text='📤 Снять экипировку')).add(
        types.KeyboardButton(text='⚒ Крафт')).add(
        types.KeyboardButton(text='🔙 Назад'))
    return reply_kb


def HEALING_Kb():
    reply_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reply_kb.add(
        types.KeyboardButton(text='💊 Лазарет')).add(
        types.KeyboardButton(text='🧪 Лечебные зелья')).add(
        types.KeyboardButton(text='🔙 Назад'))
    return reply_kb


def STATS_INC_Kb():
    kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    kb.add(types.KeyboardButton(text="⚖️ Повышение характеристик"), types.KeyboardButton(text="🔙 Назад"))
    return kb


def SHOP_Kb():
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    kb.add(
        *[types.KeyboardButton(name) for name in ('🏹 Buy armor', '🥋 Buy weapon', '🧪 Buy potion')]).add(
        types.KeyboardButton(text="🔚 Закрыть"))
    return kb


def ATTACK_Kb():
    attack_keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text="Голова", callback_data="attack_mob")
    btn2 = types.InlineKeyboardButton(text="Грудь", callback_data="attack_mob")
    btn3 = types.InlineKeyboardButton(text="Живот", callback_data="attack_mob")
    btn4 = types.InlineKeyboardButton(text="Ноги", callback_data="attack_mob")
    attack_keyboard.add(btn1, btn2, btn3, btn4)
    return attack_keyboard


def DEFENCE_Kb():
    defence_keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text="Голова", callback_data="defence_mob")
    btn2 = types.InlineKeyboardButton(text="Грудь", callback_data="defence_mob")
    btn3 = types.InlineKeyboardButton(text="Живот", callback_data="defence_mob")
    btn4 = types.InlineKeyboardButton(text="Ноги", callback_data="defence_mob")
    defence_keyboard.add(btn1, btn2, btn3, btn4)
    return defence_keyboard


def CONFIRM_BATTLE_Kb():
    kb = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton(text="⚔️ В бой!", callback_data="battle_state")
    button2 = types.InlineKeyboardButton(text="✖️ Убежать", callback_data="back")
    kb.add(button1, button2)
    return kb


def PVE_LEAVE_Kb():
    return types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('⛔️ Сдаться'))


def EQUIP_Kb(item_id):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton(text='📥 Надеть экипировку', callback_data=f"equip_{item_id}"),
           types.InlineKeyboardButton(text='🔙 Назад', callback_data=f"equip_back"))
    return kb


def UNDRESS_Kb(data):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text=f"{data[0]}", callback_data=f'unequip_{data[1]}')
    btn2 = types.InlineKeyboardButton(text=f"{data[2]}", callback_data=f'unequip_{data[3]}')
    btn3 = types.InlineKeyboardButton(text="🔙 Назад", callback_data='back')
    kb.add(btn1, btn2, btn3)
    return kb


def UPDATE_STATS_Kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        *[types.InlineKeyboardButton(x, callback_data=f'update_level_{y}') for x, y in
          {'🗡 Урон +1': 'damage', '♥ Здоровье +1': 'health', '🛡 Защита +1': 'defence'}.items()]).add(
        types.InlineKeyboardButton(text="🔚 Закрыть", callback_data='back'))
    return kb


def HEAL_CONFIRM_Kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton(text="💉 Да", callback_data="use_heal_potion"))
    kb.add(types.InlineKeyboardButton(text="🔚 Закрыть", callback_data="back"))
    return kb


def HEAL_PURCHASE_Kb(minus):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton(text=f"Приобрести -{minus} монет", callback_data="buy_heal_potion"))
    kb.add(types.InlineKeyboardButton(text="🔚 Закрыть", callback_data="back"))
    return kb


def INVENTORY_Kb(inv):
    kb = types.InlineKeyboardMarkup(row_width=1)
    for i in range(len(inv)):
        kb.add(types.InlineKeyboardButton(text=inv[i].name, callback_data=f"inv_{inv[i].id}"))
    kb.add(types.InlineKeyboardButton(text="🔚 Закрыть", callback_data="back"))
    return kb


def CRAFT_Kb(inv):
    kb = types.InlineKeyboardMarkup(row_width=1)
    for i in range(len(inv)):
        kb.add(types.InlineKeyboardButton(text=f"x2 {inv[i].name}", callback_data=f"craft_{inv[i].id}"))
    kb.add(types.InlineKeyboardButton(text="🔙 Назад", callback_data="back"))
    return kb


def HELP_Kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(*[types.InlineKeyboardButton(x, callback_data=f"help_menu_{y}") for x, y in
           {'Обучение (рекомендуется)': 'train', 'Описание игрового бота': 'desc', 'Функционал бота': 'func'}.items()])
    kb.row(types.InlineKeyboardButton(text='🔈 Прочее..', callback_data='help_menu_other'),
           types.InlineKeyboardButton(text='🔚 Закрыть', callback_data='back'))
    return kb


def FUNC_LIST_Kb():
    kb = types.InlineKeyboardMarkup(row_width=2)
    commands = ("👤 Профиль", "⚔️ Бой",
                "💉 Исцеление", "📯 Повышение ранга", "💼 Инвентарь", "📤 Снять экипировку", "🥋 Экипировка",
                "⚖️ Повышение характеристик", "⚒ Крафт", "🔈 Помощь", "🛒 Магазин")
    kb.add(*[types.InlineKeyboardButton(name, callback_data=f"help_{name}") for name in commands]).insert(
        types.InlineKeyboardButton(text="🔙 Назад", callback_data="help_back"))
    return kb


# def ADMIN_GET_Kb(matches):
#     kb = types.InlineKeyboardMarkup(row_width=1)
#     for i in range(len(matches)):
#         kb.insert(
#             types.InlineKeyboardButton(text=matches[i].username, callback_data=f"get_{matches[i].telegram_id}"))
#     return kb


def CONFIRM_Kb(text: str, callback: str):
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.row(types.InlineKeyboardButton(text=text, callback_data=callback), 
           types.InlineKeyboardButton(text='🔚 Закрыть', callback_data='back'))
    return kb


def HEALING_STATE_Kb():
    reply_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    reply_kb.add(*[
        types.KeyboardButton(text='❔ Информация'),
        types.KeyboardButton(text='🔚 Покинуть лазарет')])
    return reply_kb