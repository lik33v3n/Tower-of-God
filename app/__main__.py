import logging

from aiogram import Bot, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

from app import config

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO)
# filename='log.log', filemode='a'

logging.getLogger('gino.engine').setLevel(logging.ERROR)  # disabling gino flood


storage = MemoryStorage()
bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)


async def startup(_):
    from app.database.db import connect
    await connect()
    logging.info("*Database has been connected.")

    from app.middlewares import RegisterMiddleware, DevelopmentMiddleware
    dp.middleware.setup(DevelopmentMiddleware())
    dp.middleware.setup(RegisterMiddleware())
    logging.info('*All middlewares have been configured.')

    from app import handlers
    handlers.setup(dp)
    logging.info('*All handlers have been configured.')


async def shutdown(_):
    logging.info("*Database has been disconnected.")
    from app.database.db import disconnect
    await disconnect()
    


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=startup, on_shutdown=shutdown)
