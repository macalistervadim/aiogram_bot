from aiogram import BaseMiddleware
from typing import Any, Callable, Dict, Awaitable
from aiogram.types import Message, CallbackQuery
from aiogram.types import TelegramObject
from aiogram.types import Message

from application.database.models import async_session
from application.database.requests import get_user




