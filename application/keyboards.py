from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


from application.database.requests import get_categories

cancel = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/cancel')]
], resize_keyboard=True, input_field_placeholder='Для отмены нажмите /cancel')

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📚 Наши курсы')],
    [KeyboardButton(text='📪 Контакты')],
    [KeyboardButton(text='📨 Тех. поддержка')]
], resize_keyboard=True, input_field_placeholder='Выберите пункт ниже')



def ticket_inline_keyboard():
    ticket = InlineKeyboardBuilder()
    ticket.button(text='Закрыть', callback_data='close_ticket')
    ticket.button(text='Ответить', callback_data='answer_ticket')

    ticket.adjust(2)
    return ticket.as_markup()

def course_inline_keyboard():
    course = InlineKeyboardBuilder()
    course.button(text='Получить консультацию', callback_data='consultation')
    return course.as_markup()

async def categories():
    categories_kb = InlineKeyboardBuilder()
    categories = await get_categories()
    for category in categories:
        categories_kb.add(InlineKeyboardButton(text=category.name, callback_data=f'category_{category.id}'))
    return categories_kb.adjust(1).as_markup()
