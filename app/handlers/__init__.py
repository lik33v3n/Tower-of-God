import logging

from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.dispatcher.filters import CommandHelp, CommandStart
from aiogram.dispatcher.filters.builtin import Command, IDFilter

from ..utils.game_logic import ADMIN_COMMANDS, AVAILABLE_COMMANDS
from ..utils.states import MainStates, AdminStates
from .base_handlers import *
from .battle_handlers import *
from .game_handlers import *
from .gear_handlers import *
from .user_handlers import *


def setup(dp: Dispatcher):
    dp.register_message_handler(cmd_start, CommandStart())
    dp.register_message_handler(help_func, CommandHelp())
    dp.register_message_handler(help_func, lambda m: m.text and m.text == '🔈 Помощь')
    dp.register_callback_query_handler(help_query, lambda c: True and c.data[:5] == "help_")
    dp.register_message_handler(admin_commands, IDFilter(user_id=397247994), Command(commands=ADMIN_COMMANDS, prefixes='!'), state='*')
    dp.register_message_handler(admin_get_handler, IDFilter(user_id=397247994), state=AdminStates.getuser)
    dp.register_message_handler(IDLE, lambda m: m.text and not m.text.startswith(('!', '/')) and m.text not in AVAILABLE_COMMANDS)
    dp.register_callback_query_handler(back, lambda c: True and c.data == 'back', state='*')
    # Base handlers. ^^^
    dp.register_message_handler(pve_rankup, lambda m: m.text and m.text == '📯 Повышение ранга')
    dp.register_message_handler(pve_battle, lambda m: m.text and m.text == '⚔️ Бой')
    dp.register_callback_query_handler(pve_confirmed, lambda c: True and c.data == 'battle_state', state=MainStates.battle)
    dp.register_callback_query_handler(pve_attack, lambda c: True and c.data == 'attack_mob', state='*')
    dp.register_callback_query_handler(pve_defence, lambda c: True and c.data == 'defence_mob', state='*')
    dp.register_message_handler(pve_leave_battle, lambda m: m.text and m.text == '⛔️ Сдаться', state=MainStates.battle)
    # Battle handlers. ^^^
    dp.register_message_handler(shop_func, lambda m: m.text and m.text == '🛒 Магазин')
    dp.register_message_handler(shop_query, lambda m: m.text and m.text in ('🏹 Buy armor', '🥋 Buy weapon', '🧪 Buy potion'), state=MainStates.shopping)
    dp.register_callback_query_handler(buy_heal_potion, lambda c: True and c.data == 'buy_heal_potion')
    # Game handlers. ^^^
    dp.register_message_handler(gear_info_check, lambda m: m.text and m.text.startswith('/'))
    dp.register_callback_query_handler(gear_equip, lambda c: True and c.data[:6] == 'equip_')
    dp.register_message_handler(gear_unequip, lambda m: m.text and m.text == '📤 Снять экипировку')
    dp.register_callback_query_handler(gear_unequip_query, lambda c: True and c.data[:8] == 'unequip_' and c.data[8:] != 'empty')
    dp.register_message_handler(gear_craft, lambda m: m.text and m.text == '⚒ Крафт')
    dp.register_callback_query_handler(gear_craft_query, lambda c: True and c.data[:6] == 'craft_')
    # Gear handlers. ^^^
    dp.register_message_handler(user_profile, lambda m: m.text and m.text == '👤 Профиль')
    dp.register_message_handler(user_inventory, lambda m: m.text and m.text == '💼 Инвентарь')
    dp.register_callback_query_handler(user_inventory_items, lambda c: True and c.data[:4] == 'inv_')
    dp.register_message_handler(user_equipment, lambda m: m.text and m.text == '🥋 Экипировка')
    dp.register_message_handler(user_heal, lambda m: m.text and m.text == '💉 Исцеление')
    dp.register_callback_query_handler(user_heal_query, lambda c: True and c.data == 'use_heal_potion')
    dp.register_message_handler(user_stats_increase, lambda m: m.text and m.text == '⚖️ Повышение характеристик')
    dp.register_callback_query_handler(user_stats_increase_query, lambda c: True and c.data[:13] == 'update_level_')
    # User handlers. ^^^
