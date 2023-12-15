from aiogram.fsm.state import StatesGroup, State


class Support(StatesGroup):
    question = State()
    wait = State()

class AnswerQuestion(StatesGroup):
    ticket_number = State()
    answer = State()
