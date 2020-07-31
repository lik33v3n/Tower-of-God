from aiogram.dispatcher.filters.state import State, StatesGroup


class MainStates(StatesGroup):
    battle = State()
    selling = State()
    shopping = State()
    healing = State()

class AdminStates(StatesGroup):
    getuser = State()
    deluser = State()
