import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import router


BOT_TOKEN = "Введите ваш токен бота здесь"  # Замените на ваш токен бота

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)


async def main():
    async with Bot(token=BOT_TOKEN) as bot:
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())