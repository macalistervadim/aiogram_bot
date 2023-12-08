from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from sqlalchemy.ext.asyncio import AsyncSession

import application.keyboards as kb
import application.states as st
from application.database.requests import add_user
from application.database.models import async_session

router = Router()

#router.message.outer_middleware(RegistrationMiddleware())

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