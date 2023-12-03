from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

import application.keyboards as kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}\n'
                         f'Для дальнейшего использования бота, Вам необходимо'
                         f'пройти регистрацию', reply_markup=kb.registration)

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