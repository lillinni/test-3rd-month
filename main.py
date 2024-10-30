# main.py
import asyncio 
import logging 
from aiogram import Bot

from bot_config import bot, dp, database
from handlers.bot_fsm import bot_fsm_router

async def on_startup(bot: Bot):
    print('Бот запустился')
    database.create_tables()

async def main():
    dp.include_router(bot_fsm_router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot) 
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

