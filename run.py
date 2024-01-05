import logging
import sys
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Bot, Dispatcher

from application.middleware import CheckTime, SupportWait
from application.handlers import router
from application.database.models import async_main
from config import TOKEN
from application.admin import auto_reklama

async def main():
    await async_main()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

    scheduler.add_job(auto_reklama, "interval", hours=6, kwargs={'bot': bot})

    dp.message.middleware(SupportWait())
    dp.message.middleware(CheckTime())

    scheduler.start()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
