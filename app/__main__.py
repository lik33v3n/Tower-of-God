import logging

from aiogram import Bot, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

from app import config

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', 
                    level=logging.INFO, 
                    handlers=[logging.FileHandler(filename="log.log", encoding='utf8'), 
                            logging.StreamHandler()])
                    
logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger("gino.engine").setLevel(logging.ERROR)


storage = MemoryStorage()
bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)


async def startup(_):
    from app.utils.scheduler import scheduler
    scheduler.start()

    from app.database.db import connect
    await connect()
    logging.info("*Database was connected.")

    from app.middlewares import RegisterMiddleware, DevelopmentMiddleware
    dp.middleware.setup(DevelopmentMiddleware())
    dp.middleware.setup(RegisterMiddleware())
    logging.info("*All middlewares were configured.")

    from app import handlers
    handlers.setup(dp)
    logging.info("*All handlers were configured.")


async def shutdown(_):
    logging.info("*Database was disconnected.")
    from app.database.db import disconnect
    await disconnect()

    from app.utils.scheduler import scheduler
    scheduler.shutdown(wait=False)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, 
                               on_startup=startup, 
                               on_shutdown=shutdown)
