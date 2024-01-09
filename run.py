import logging
import sys
import asyncio

from aiogram.filters import Command
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Bot, Dispatcher

from application.filters.is_admin import IsAdminFilter
from application.middleware import CheckTime, SupportWait
from application.handlers import router
from application.database.models import async_main
from config import TOKEN
from application.admin import auto_reklama, reklama_2, mailing

# ПРОМОКОДЫ

async def main():
    await async_main()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

    scheduler.add_job(auto_reklama, "interval", hours=6, kwargs={'bot': bot})
    scheduler.add_job(reklama_2, "interval", hours=8, kwargs={'bot': bot})

    dp.message.middleware(SupportWait())
    dp.message.middleware(CheckTime())

    async def mailing_handler(message: Message):
        await mailing(message, bot)

    dp.message.register(mailing_handler, Command('mailing'))


    scheduler.start()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
