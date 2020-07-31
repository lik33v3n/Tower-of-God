import logging
from contextlib import suppress

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import (BotBlocked, MessageCantBeDeleted,
                                      MessageToDeleteNotFound)

from app.database.user import User


class RegisterMiddleware(BaseMiddleware):
    async def return_user(self, data: dict, base_user: types.User):
        user = await User.get(base_user.id)
        if user is None: 
            with suppress(BotBlocked):
                user = await User.create(id=base_user.id, username=base_user.first_name)
                logging.info(f"New user: {base_user.id}, {base_user.first_name}.")

        data["user"] = user

    async def on_pre_process_message(self, m: types.Message, data: dict):
        await self.return_user(data, m.from_user)
        print(f"[M] \"{m.text}\"  -  {m.from_user.id} | {m.from_user.first_name}")
        if m.text == '~':
            with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
                await m.delete()

    async def on_pre_process_callback_query(self, c: types.CallbackQuery, data: dict):
        await self.return_user(data, c.from_user)
        print(f"[Q] \"{c.data}\"  -  {c.from_user.id} | {c.from_user.first_name}")
