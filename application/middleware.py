import logging
from datetime import datetime, time
from aiogram import BaseMiddleware
from typing import Any, Callable, Dict, Awaitable

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, TelegramObject

from application.states import Support

class SupportWait(BaseMiddleware):
    # Мидлварь ожидания техподдержки
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        state: FSMContext = data.get("state")
        current_state = await state.get_state()

        logging.info(current_state)

        if current_state == Support.wait:
            await event.answer('Вы в режиме ожидания!')
        else:
            return await handler(event, data)

class CheckTime(BaseMiddleware):
    #Проверка часов работы бота
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        start_time = time(10, 0)
        end_time = time(19, 0)

        if start_time <= datetime.now().time() <= end_time:
            return await handler(event, data)
        return event.answer('Упс!\n\n'
                            'К сожалению, время работы нашего бота вышло.\n'
                            'Время работы бота: с 10:00 до 18:00')

