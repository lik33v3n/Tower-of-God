from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from ..database.base import User, Ability


rank_boost = {'F': 0.1, 'E': 0.2, 'D': 0.3, 'C': 0.4, 'B': 0.5, 'A': 0.6, 'S': 0.7}

class AbilityMethods(object):
    async def neptunes_wrath(self, call: CallbackQuery, user: User, ability, state: FSMContext):
        await user.update(health=user.max_health).apply()
        await call.answer(text=f'success')
