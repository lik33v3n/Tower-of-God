from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from dateutil.relativedelta import relativedelta

from ..database.base import User
from ..helpers.keyboards import SHOP_Kb
from ..utils.states import MainStates


async def shop_func(m: Message):
    await MainStates.shopping.set()
    time = datetime.now().strftime('|%Y-%m-%d %H:%M:%S|')
    await m.answer(f'{time} Shop:', reply_markup=SHOP_Kb())


async def shop_query(m: Message, state: FSMContext):
    time = datetime.now()
    if m.text == '🏹 Buy armor':
        update_time = time.strftime('%Y-%m-%d 23:59:59')
        upt = datetime.strptime(update_time, '%Y-%m-%d %H:%M:%S')
        diff = relativedelta(upt, time)
        await m.answer(
            f"Сейчас: {time.strftime('|%H:%M:%S|')}, до обновления: |{diff.hours}:{diff.minutes}:{diff.seconds}|")
    elif m.text == '🥋 Buy weapon':
        pass
    elif m.text == '🧪 Buy potion':
        pass
    else:
        await state.reset_state()


async def buy_heal_potion(c: CallbackQuery, user: User):
    if user.balance - (user.lvl * 10) // 4 >= 0:
        await user.update(heal_potions=user.heal_potions+1, balance=user.balance - (user.lvl * 10) // 4).apply()
        await c.message.edit_text(
            f'❕ Вы преобрели 1 лечебное зельё, с вашего баланса списано {(user.lvl * 10) // 4} монет.')
    else:
        await c.message.edit_text('❗ У вас недостаточно монет')
