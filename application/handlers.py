from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
import application.keyboards as kb
import application.states as st
from application.database.requests import add_user, add_ticket, get_ticket, close_ticket_in_database
from application.database.models import async_session


router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    async with async_session() as session:
        await add_user(session, tg_id=message.from_user.id)

    await message.answer(f'Привет, {message.from_user.full_name}\n', reply_markup=kb.main)

@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите вариант из каталога', reply_markup=await kb.categories())

@router.callback_query(F.data.startswith('category_'))
async def category_selected(callback: CallbackQuery):
    category_id = callback.data.split('_')[1]
    await callback.message.answer(f'Товары по выбранной категории: ', reply_markup=await kb.products(category_id))
    await callback.answer('')

@router.callback_query(F.data.startswith('product_'))
async def product_selected(callback: CallbackQuery):
    product_id = callback.data.split('_')[1]
    await callback.message.answer(f'Ваш товар {product_id}')
    await callback.answer('')

@router.message(StateFilter(None), F.text == 'Тех. поддержка')
async def support(message: Message, state: FSMContext):
    await message.answer('Добро пожаловать в раздел Технической поддержки.\n'
                         'Здесь Вы можете найти ответы на интересующие Вас вопросы.\n\n'
                         'Пожалуйста, для продолжения, напишите свой вопрос (для отмены - /cancel): ',
                                                                                            reply_markup=kb.cancel)
    await state.set_state(st.Support.question)

@router.message(st.Support.question)
async def question(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(question=message.text.lower())

    ticket = await add_ticket(tg_id=message.from_user.id)
    if ticket != False:
        await bot.send_message('5046166133', f'Пришел новый тикет от @{message.from_user.username}'
                                             f' №{ticket}\n\n' + message.text, reply_markup=kb.ticket_inline_keyboard())

        await message.answer('Спасибо! Мы уже приняли Ваш вопрос и работаем над ним.\n\n'
                             'В данный момент вы были переброшены в режим "Ожидания" - '
                             'в данном режиме недоступны никакие команды. После того, как Ваш вопрос будет решён - '
                             'Вас автоматически уберет из режима ожидания наш бот. Спасибо за понимание.\n'
                             f'Вы в очереди - {ticket}\n\n'
                             'Если Вы создали ошибочный тикет, пожалуйста, отмените его командой - /cancel',
                                                                             reply_markup=kb.cancel)
    else:
        await message.answer('Вы уже создавали тикет!')
        await state.clear()

@router.callback_query(F.data.startswith('answer_'))
async def answer_ticket_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите номер тикета, на который хотите ответить:', reply_markup=kb.cancel)

    await state.set_state(st.AnswerQuestion.ticket_number)

@router.message(st.AnswerQuestion.ticket_number)
async def answer_ticket_2(message: Message, state: FSMContext):
    await state.update_data(ticket_number=message.text.lower())

    await message.answer('Введите ответ на тикет: ')

    await state.set_state(st.AnswerQuestion.answer)

@router.message(st.AnswerQuestion.answer)
async def answer_ticket_3(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(answer=message.text.lower())

    data = await state.get_data()
    ticket_id = data.get('ticket_number')
    try:
        tg_id = await get_ticket(ticket_id)
        await close_ticket_in_database(ticket_id)
        await bot.send_message(tg_id, f'Ответ от Агента Поддержки по вопросу №{ticket_id}\n\n'
                               + data.get("answer"))

        await message.answer('Ваш ответ успешно отправлен пользователю')
        await state.clear()
    except Exception:
        await message.answer('Такого тикета не существует.\n'
                             'Операция прервана')
        await state.clear()


