from aiogram.filters import BaseFilter
from aiogram.types import Message

import config


class IsAdminFilter(BaseFilter):
    """
    Проверка на администратора
    """
    async def __call__ (self, message: Message):
        try:
            return message.from_user.id == config.ADMIN_ID
        except:
            return False
