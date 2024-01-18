import phonenumbers

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter

import application.keyboards as kb
import application.states as st
import config
from application.database.requests import (add_user, add_ticket, get_ticket, close_ticket_in_database,
                                           get_course, get_ticket_id, activation_pcode)
from application.database.models import async_session

router = Router()


@router.message(F.text == '/cancel')
async def cancel(message: Message, state: FSMContext):
    ticket_user = await get_ticket_id(message.from_user.id)

    await state.clear()
    await message.answer('✔️ Ваш текущий запрос был отменен.')
    if ticket_user:
        await close_ticket_in_database(ticket_user)

@router.message(CommandStart())
async def cmd_start(message: Message):
    async with async_session() as session:
        await add_user(session, tg_id=message.from_user.id)

    await message.answer('🚀 Добро пожаловать в нашу онлайн-школу по программированию! 🌐💻\n\n'
                         'Здесь ты откроешь для себя увлекательный мир кодинга, где творчество и технологии встречаются. Независимо от того, начинающий ты или опытный программист, у нас есть что-то интересное для каждого.\n\n'
                         '👨‍💻 Наши курсы охватывают различные языки программирования, фреймворки и технологии. Мы стремимся сделать обучение доступным и увлекательным, чтобы каждый мог развивать свои навыки.\n\n'
                         '👩‍🏫 Следи за нашими уроками, мастер-классами и событиями, чтобы быть в курсе последних тенденций в мире IT.\n\n'
                         '🤖 Для начала, давай начнем с чего-то простого! Введите /start, чтобы получить список доступных курсов и начать свой учебный путь.\n\n'
                         'Не стесняйся задавать вопросы! Мы здесь, чтобы помочь тебе стать настоящим мастером кода.\n Удачи в учебе! 🌟', reply_markup=kb.main)

@router.message(F.text == '📪 Контакты')
async def catalog(message: Message):
    await message.answer('🔹 Контакты нашей онлайн-школы:\n\n'
                         'Номер телефона: +7 900 00 000\n'
                         'Email: online@hotmail.com\n'
                         'Сайт: online-school.com\n\n'
                         '🔹 Если остались какие-либо вопросы - наша Техническая поддержка всегда готова Вам помочь.',
                         reply_markup=kb.main)

@router.message(F.text == '📚 Наши курсы')
async def catalog(message: Message):
    await message.answer('Выберите вариант из каталога', reply_markup=await kb.categories())

@router.callback_query(F.data.startswith('category_'))
async def get_courses(callback: CallbackQuery):
    category_id = callback.data.split('_')[1]  # Получаем идентификатор категории
    courses = await get_course(category_id)
    if courses:
        for course in courses:
            await callback.message.answer('Отличный выбор, вот описание выбранного Вами курса:\n\n'
                                          f'🎲 Название курса: {course.name}\n'
                                          f'🐶 Преподаватель: {course.teacher}\n'
                                          f'🕓 Курс действителен до: {course.duration}\n'
                                          f'✔️ Описание {course.description}\n\n'
                                          f'💰 Цена: {course.price}руб. ежемесячно\n\n'
                                          f'Если Вас заинтересовал данный курс, Вы можете бесплатно'
                                          f'получить консультацию у наших специалистов, которые подберут'
                                          f'программу курса специально под Вас! Для записи на'
                                          f'консультацию нажмите кнопку ниже: ', reply_markup=kb.course_inline_keyboard())


@router.message(StateFilter(None), F.text == '📨 Тех. поддержка')
async def support(message: Message, state: FSMContext):
    await message.answer('🔕 Добро пожаловать в раздел Технической поддержки.\n'
                         'Здесь Вы можете найти ответы на интересующие Вас вопросы.\n\n'
                         'Пожалуйста, для продолжения, напишите свой вопрос (для отмены - /cancel): ',
                                                                                            reply_markup=kb.cancel)
    await state.set_state(st.Support.question)

@router.message(st.Support.question)
async def question(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(question=message.text.lower())

    ticket = await add_ticket(tg_id=message.from_user.id)
    if ticket != False:
        await bot.send_message(config.ADMIN_ID, f'🔔 Пришел новый тикет от @{message.from_user.username}'
                                             f' №{ticket}\n\n' + message.text, reply_markup=kb.ticket_inline_keyboard())

        await message.answer('Спасибо! Мы уже приняли Ваш вопрос и работаем над ним.\n\n'
                             'В данный момент вы были переброшены в режим "Ожидания" - '
                             'в данном режиме недоступны никакие команды. После того, как Ваш вопрос будет решён - '
                             'Вас автоматически уберет из режима ожидания наш бот. Спасибо за понимание.\n'
                             f'Вы в очереди - {ticket}\n\n'
                             '🔺 Если Вы создали ошибочный тикет, пожалуйста, отмените его командой - /cancel',
                                                                             reply_markup=kb.cancel)
    else:
        await message.answer('🔺 Вы уже создавали тикет!')
        await state.clear()

@router.callback_query(F.data.startswith('answer_'))
async def answer_ticket_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('🔺 Введите номер тикета, на который хотите ответить:', reply_markup=kb.cancel)

    await state.set_state(st.AnswerQuestion.ticket_number)

@router.message(st.AnswerQuestion.ticket_number)
async def answer_ticket_2(message: Message, state: FSMContext):
    await state.update_data(ticket_number=message.text.lower())

    await message.answer('🔺 Введите ответ на тикет: ')

    await state.set_state(st.AnswerQuestion.answer)

@router.message(st.AnswerQuestion.answer)
async def answer_ticket_3(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(answer=message.text.lower())

    data = await state.get_data()
    ticket_id = data.get('ticket_number')
    try:
        tg_id = await get_ticket(ticket_id)
        await close_ticket_in_database(ticket_id)
        await bot.send_message(tg_id, f'📣 Ответ от Агента Поддержки по вопросу №{ticket_id}\n\n'
                               + data.get("answer"))

        await message.answer('📣 Ваш ответ успешно отправлен пользователю')
        await state.clear()
    except Exception:
        await message.answer('Такого тикета не существует.\n'
                             'Операция прервана')
        await state.clear()


@router.callback_query(F.data.startswith('consultation'))
async def consultation_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('☎️ Отличный выбор!\n\n'
                                  'Для получения дальнейшей консультации по выбранному курсу, Вам'
                                  'необходимо прикрепить свой номер телефона для связи с вами.\n'
                                  'Пожалуйста, напишите свой номер телефона в следующем формате:\n\n'
                                  '+X {код страны} ХХХ {код штата или города} ХХХХ-ХХ-ХХ {номер абонента}\n')

    await state.set_state(st.GetConsultation.number)

@router.message(st.GetConsultation.number)
async def get_consultation_number(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(phone=message.text.lower())
    data = await state.get_data()
    try:
        parsed_number = phonenumbers.parse(data.get('phone'), None)
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError("Invalid phone number")
        await message.answer('♦️ У вас есть специальный промокод? (если нет - введите 0)')
        await state.set_state(st.GetConsultation.pcode)
    except Exception as e:
        await message.answer('Некорректный номер телефона. Пожалуйста, используйте формат: +X ХХХХХХХХХХ.')
        await state.set_state(st.GetConsultation.number)
        return

@router.message(st.GetConsultation.pcode)
async def get_consultation_pcode(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(pcode=message.text.lower())
    data = await state.get_data()


    if message.text.lower() != '0':
        session, get_p = await activation_pcode(message.text.lower())
        if get_p is None:
                await message.answer('Такого промокода не существует, попробуйте заново или введите - 0')
                await state.set_state(st.GetConsultation.pcode)
                return
    await state.update_data(pcode=message.text.lower())

    await bot.send_message(config.ADMIN_ID, '🔔 Пришел запрос на консультацию по курсу.\n'
                                                        f'Номер телефона: {data.get("phone")}\n'
                                                        f'Промокод: {data.get("pcode")}')

    await message.answer('🔔 Ваш запрос на консультацию успешно принят!\n\n'
                                     'В ближайшее время с Вами свяжется наш Агент поддержки и проконсультирует Вас '
                                     'по интересующему вопросу. Пожалуйста, ожидайте')
    await state.clear()

@router.callback_query(F.data.startswith('close_'))
async def answer_ticket_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('🔺 Введите номер тикета, который хотите закрыть:', reply_markup=kb.cancel)

    await state.set_state(st.CloseTicket.ticket_number)

@router.message(st.CloseTicket.ticket_number)
async def close_ticket_2(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(ticket_number=message.text.lower())

    data = await state.get_data()
    ticket_id = data.get('ticket_number')

    try:
        tg_id = await get_ticket(ticket_id)
        await close_ticket_in_database(ticket_id)
        await bot.send_message(tg_id, f'📣 Ваш тикет №{ticket_id} был закрыт Агентом Поддержки')
        await message.answer(f'🔺 Вы успешно закрыли тикет №{ticket_id}')

        await state.clear()

    except Exception:
        await message.answer('🔺 Данного тикета не существует')

        await state.clear()
