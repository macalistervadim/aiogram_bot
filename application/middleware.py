import logging
from datetime import datetime, time
from aiogram import BaseMiddleware
from typing import Any, Callable, Dict, Awaitable
from aiogram.types import Message

from application.states import Support
from application.database.requests import get_ticket_user

class SupportWait(BaseMiddleware):
    # Мидлварь ожидания техподдержки
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user_id = data['event_from_user'].id
        try:
            current_user = await get_ticket_user(user_id)
        except Exception:
            pass

        if data['event_update'].message.text == '/cancel':
            return await handler(event, data)
        elif current_user == user_id:
            await event.answer('Упс.\n\n'
                               'Кажется Вы находитесь в режиме "ожидания".\n'
                               'Пожалуйста, ожидайте ответа на свой вопрос, чтобы выйти из режима ожидания')
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

        start_time = time(8, 0)
        end_time = time(21, 0)

        if start_time <= datetime.now().time() <= end_time:
            return await handler(event, data)
        return event.answer('Упс!\n\n'
                            'К сожалению, время работы нашего бота вышло.\n'
                            'Время работы бота: с 8:00 до 21:00')

