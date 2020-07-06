from aiogram.dispatcher.filters.state import State, StatesGroup


class MainStates(StatesGroup):
    battle = State()
    shopping = State()

class AdminStates(StatesGroup):
    getuser = State()
