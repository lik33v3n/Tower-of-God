from gino import Gino

from app import config
import logging

db = Gino()


async def connect():
    await db.set_bind(config.POSTGRES_URI)


async def disconnect():
    bind = db.pop_bind()
    if bind:
        await bind.close()
