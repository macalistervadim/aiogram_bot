from aiogram import Bot
from aiogram.types import Message
from aiogram.utils.markdown import hide_link

from application.database.requests import get_users

async def auto_reklama(bot: Bot):
    users = await get_users()

    for i in users:
        await bot.send_message(i,
                               f'{hide_link("https://sun108-2.userapi.com/impg/iwoHyvcmgSGDgY0cHfd3jJstqWJny2Pdso2SJw/ykABvQ4T74k.jpg?size=2560x1692&quality=95&sign=f6c42e6b5c5e177427eef64812b209bc&type=album")}'
                               f'Уважаемые пользователи\n\n'
                               f'Мы предлагаем Вам посетить нашу <a href="https://vk.com/phoenixstudio_off"> группу ВКонтакте</a>, где Вы можете'
                               f'найти для себя много нового и интересного контента, связанного с разработками'
                               f'готовых решений для Ваших продуктов.\n\n'
                               f'Мы с нетерпением ждем Вас в нашем интересном сообществе 😉', parse_mode='HTML')