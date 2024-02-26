import config
from bot import bot, dp
from aiogram.utils import executor
from handlers import admin
from handlers import client


async def main(_):#Функция выполняется при запуске
    for admin in config.ADMINS:
        try:
            await bot.send_message(admin, 'Бот запущен!')
        except:
            pass

executor.start_polling(dp, on_startup=main)