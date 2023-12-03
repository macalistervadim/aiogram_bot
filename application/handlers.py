from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter

import application.keyboards as kb
import application.states as st

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}\n'
                         f'Для дальнейшего использования бота, Вам необходимо'
                         f'пройти регистрацию', reply_markup=kb.registration)

@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите вариант из каталога', reply_markup=await kb.categories())

@router.message(StateFilter(None), F.text == 'Зарегистрироваться')
async def registration(message: Message, state: FSMContext):
    await message.answer('Введите Ваше имя:')

    await state.set_state(st.Registration.f_name)

@router.message(st.Registration.f_name)
async def registration_2(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text.capitalize())
    await message.answer('Введите Вашу фамилию: ')

    await state.set_state(st.Registration.l_name)

@router.message(st.Registration.l_name)
async def registration_2(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text.capitalize())
    await message.answer('Введите Ваш номер телефона (для пропуска - 0): ')

    await state.set_state(st.Registration.l_name)

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