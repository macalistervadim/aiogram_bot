import logging

from aiogram import BaseMiddleware
from typing import Any, Callable, Dict, Awaitable

from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.types import Message, CallbackQuery
from aiogram.types import TelegramObject
from aiogram.types import Message

from application.database.models import async_session
from application.database.requests import get_user
from application.states import Support

class SupportWait(BaseMiddleware):
    # Мидлварь ожидания техподдержки
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        state = data.get('state')

        logging.info(f'State: {state}')

        if state == Support.wait:
            await event.answer('Вы в режиме ожидания!')
        else:
            return await handler(event, data)



