from collections import deque
from contextlib import suppress
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types.chat import ChatActions
from aiogram.utils.exceptions import CantParseEntities, MessageNotModified, MessageToDeleteNotFound

from ..database.db import db
from ..database.user import User
from ..handlers.user_handlers import user_profile
from ..helpers.keyboards import ADMIN_GET_Kb, FUNC_LIST_Kb, HELP_Kb, IDLE_Kb
from ..helpers.scenario import func_description, greetings, help_text


async def cmd_start(m: Message, user: User):
    for i in range(8):
        await m.answer(greetings[i])
        await ChatActions().typing(sleep=1.5)
    await user_profile(m, user, False)


async def help_func(m: Message):
    await m.answer('❕ Нажмите на любой раздел:', reply_markup=HELP_Kb())


async def help_query(c: CallbackQuery):
    try:
        if c.data == 'help_menu_func':
            await c.message.edit_text('Весь функционал игрового бота: (нажмите для информации)',
                                      reply_markup=FUNC_LIST_Kb())
        if c.data[:10] == 'help_menu_' and c.data[10:] != 'func':
            await c.message.edit_text(help_text.get(c.data[10:]), reply_markup=HELP_Kb())
        elif c.data[5:] != "back":
            await c.answer(func_description.get(c.data[5:]), show_alert=True)
        else:
            await c.message.edit_text('❕ Нажмите на любой раздел:', reply_markup=HELP_Kb())
    except MessageNotModified:
        pass


async def admin_commands(m: Message):
    if m.text == '!lambda':
        await m.reply('Available commands:\n <b>!get</b> \'column\' \'value\'\n <b>!log</b> \'rows\'')
    elif m.text == '!info':
        count = await db.func.count(User.id).gino.scalar() # pylint: disable=no-member
        time = datetime.now().strftime('|%d.%m.%y - %H:%M|')
        await m.reply(f"<b>Server time:</b> {time}\n<b>User count:</b> {count}")
    elif '!log' in m.text:
        data = ''
        with open('log.log', 'r') as log:
            try:
                for row in deque(log, int(m.text[4:])):
                    data += f'{row}'
                await m.reply(text=data)
            except (ValueError, CantParseEntities) as err:
                await m.reply(f'<b>{err.__class__.__name__}</b> - Введи правильное число строк!')
    elif '!get' in m.text: 
        # try:
        #     lst = m.text.split(' ')
        #     lst[2] = lst[2].replace('_', ' ')
        #     result, check = await mysql.read(f"SELECT * FROM users WHERE {lst[1]} LIKE '{lst[2]}%'")
        #     if check != 0:
        #         await m.reply(f'❕ Все совпадения \"{lst[1]} LIKE {lst[2]}%\"', reply_markup=ADMIN_GET_Kb(result))
        #     else:
        #         await m.reply('❗ Ничего не найдено')
        # except Exception as err:
        #     await m.reply(err.__class__.__name__)
        pass
    elif '!deluser' in m.text:
        # try:
        #     lst = m.text.split(' ')
        #     lst[1] = lst[1].replace('_', ' ')
        #     await User.query.filter(User.id == lst[1]).delete()
        #     await m.answer(f'{lst[1]} was successfully removed from the game!')
        # except Exception as err:
        #     await m.reply(err.__class__.__name__)
        pass


async def admin_get_query(c: CallbackQuery):
    gotcha = await User.get(c.data[4:])
    if gotcha:
        with suppress(MessageToDeleteNotFound):
            await c.message.delete()
        await user_profile(c.message, gotcha, False)
    else:
        await c.answer(text="<b>Error:</b> Игрока с таким ид не существует | Свяжитесь с администрацией")


async def IDLE(m: Message, user: dict):
    await m.answer('Главное меню <b>“Tower of God”</b>.', reply_markup=IDLE_Kb())


async def back(c: CallbackQuery, state: FSMContext):
    with suppress(MessageToDeleteNotFound):
        await c.message.delete()
    await state.reset_state()
    async with state.proxy() as data:
        data['enemy'] = {}
    await c.message.answer('Главное меню <b>“Tower of God”</b>.', reply_markup=IDLE_Kb())


# @dp.errors_handler()
# async def errors_handler(update: types.Update, exception: Exception):
#     try:
#         raise exception
#     except Exception as e:
#         logging.error(f"[TOWER] \"Exception {e} in update\" {update.update_id} | ")
#     return True
