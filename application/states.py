from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    f_name = State()
    l_name = State()
    phone = State()
