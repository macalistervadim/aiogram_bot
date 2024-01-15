from aiogram.fsm.state import StatesGroup, State


class Support(StatesGroup):
    question = State()
    wait = State()

class AnswerQuestion(StatesGroup):
    ticket_number = State()
    answer = State()

class CloseTicket(StatesGroup):
    ticket_number = State()

class GetConsultation(StatesGroup):
    number = State()
    pcode = State()

class AddPcode(StatesGroup):
    pcode = State()
    validity = State()
    discount = State()
