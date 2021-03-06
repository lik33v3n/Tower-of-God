import asyncio
import logging
from collections import deque
from contextlib import suppress
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, Update
from aiogram.types.chat import ChatActions
from aiogram.utils.exceptions import (BadRequest, BotBlocked,
                                      CantParseEntities, ChatNotFound,
                                      MessageNotModified,
                                      MessageToDeleteNotFound,
                                      MessageToReplyNotFound, RetryAfter,
                                      TelegramAPIError, UserDeactivated)
from aiogram.utils.markdown import quote_html

from ..__main__ import bot
from ..database.db import db
from ..database.user import User
from ..handlers.user_handlers import user_profile
from ..helpers.keyboards import FUNC_LIST_Kb, HELP_Kb, IDLE_Kb
from ..helpers.scenario import func_description, greetings, help_text
from ..utils.states import AdminStates


async def cmd_start(m: Message, user: User):
    for i in range(8):
        await m.answer(greetings[i])
        await ChatActions().typing(sleep=1.5)
    await user_profile(m, user, False)


async def send_message(user_id: int, text: str, disable_notification: bool = False) -> bool:
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)
    except BotBlocked:
        logging.error(f"Target [ID:{user_id}]: blocked by user")
    except ChatNotFound:
        logging.error(f"Target [ID:{user_id}]: invalid user ID")
    except RetryAfter as e:
        logging.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)
    except UserDeactivated:
        logging.error(f"Target [ID:{user_id}]: user is deactivated")
    except TelegramAPIError:
        logging.exception(f"Target [ID:{user_id}]: failed")
    else:
        logging.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcaster(text: str, disable_notification: bool) -> int:
    count = 0
    user_list = await User.select('id').gino.all()
    user_count = await db.func.count(User.id).gino.scalar() # pylint: disable=no-member
    try:
        for user_id in user_list:
            if await send_message(user_id=user_id[0], text=text, disable_notification=disable_notification):
                count += 1
            await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
    finally:
        logging.info(f"{count} messages successful sent.")

    return count, user_count



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
    if m.text == '!info':
        count = await db.func.count(User.id).gino.scalar() # pylint: disable=no-member
        time = datetime.now().strftime('|%d.%m.%y - %H:%M|')
        await m.reply(f"<b>Server time:</b> {time}\n<b>User count:</b> {count}")
    elif '!log' in m.text:
        data = ''
        with open('log.log', 'r') as log:
            try:
                for row in deque(log, int(m.text[4:])):
                    data += quote_html(row)
                await m.reply(data)
            except (ValueError) as err:
                await m.reply(f'<b>{err.__class__.__name__}</b> - Введи правильное число строк!')
    elif '!get' in m.text: 
        if len(m.text) > 4:
            lst = m.text.split(' ')
            result = await User.get(int(lst[1]))
            if result:
                m.from_user.first_name = result.id
                await user_profile(m, result, False)
            else:
                await m.reply('❗ Ничего не найдено')
        elif m.text == '!get':
            await AdminStates.getuser.set()
            await m.reply("Перешли любое сообщение от юзера.")
    elif '!deluser' in m.text:
        if m.text == '!deluser':
            await AdminStates.deluser.set()
            await m.reply("Перешли любое сообщение от юзера.")
    elif '!reload' == m.text:
        count, user_count = await broadcaster(text='❗ Бот будет перезагружен через через (1) минуту. <i>Рекомендуется покинуть бой/торговую площадку/лазарет</i>.', disable_notification=False)
        await m.reply(f'❕ Ваше сообщение получили {count}/{user_count} пользователя/ей.')    
    elif m.text[:10] == '!broadcast' or m.text[:11] == '!sbroadcast':
        text = m.text.split(' ', 1)
        count, user_count = await broadcaster(text=text[1], disable_notification=False if text[0] == '!broadcast' else True)
        await m.reply(f'❕ Ваше сообщение получили {count}/{user_count} пользователя/ей.')



async def admin_get_handler(m: Message, state: FSMContext):
    if m.forward_from:
        result = await User.get(m.forward_from)
        if result:
            m.from_user.first_name = f'{m.forward_from.id}({m.forward_from.first_name})'
            await user_profile(m, result, False)
        else:
            await m.reply('❗ Юзер не зарегистрирован.')
    else:
        await m.reply('❗ ПЕРЕШЛИ СООБЩЕНИЕ')
    await state.reset_state()


async def admin_del_handler(m: Message, state: FSMContext):
    if m.forward_from:
        result = await User.get(m.forward_from)
        if result:
            try:
                await User.delete.where(User.id == result.id).gino.first()
                await m.answer(f'{result.id} was successfully removed from the game!')
            except Exception as err:
                await m.reply(err.__class__.__name__)
                raise err
        else:
            await m.reply('❗ Юзер не зарегистрирован.')
    else:
        await m.reply('❗ ПЕРЕШЛИ СООБЩЕНИЕ')
    await state.reset_state()


async def IDLE(m: Message, user: dict):
    await m.answer('Главное меню <b>“Tower of God”</b>.', reply_markup=IDLE_Kb())


async def back(c: CallbackQuery, state: FSMContext):
    with suppress(MessageToDeleteNotFound):
        await c.message.delete()
    await state.reset_state()
    await state.reset_data()
    await c.message.answer('Главное меню <b>“Tower of God”</b>.', reply_markup=IDLE_Kb())


async def errors_handler(update: Update, exception: Exception):
    try:
        raise exception
    except Exception as e:
        time = datetime.now().strftime('%d.%m.%y - %H:%M:%S')
        with suppress(AttributeError, MessageToReplyNotFound, BadRequest):
            await update.message.reply(f'Произошла ошибка: <b>{e.__class__.__name__}</b>.\nTraceback: \"<i>{e}</i>\".'
                                       f'\nВремя ошибки: <b>{time}</b> \n<i>Cообщите администрации - @likeeven</i>')
