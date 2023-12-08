import logging
import sys
import asyncio

from aiogram import Bot, Dispatcher

from application.handlers import router
from application.database.models import async_main
from config import TOKEN

async def main():
    await async_main()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
