from aiogram.fsm.state import StatesGroup, State


class Support(StatesGroup):
    question = State()
    wait = State()
