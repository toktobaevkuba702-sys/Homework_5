import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

BOT_TOKEN = "Введите сюда свой токен бота"

dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}, я твой бот!"
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "/start — команда для запуска\n"
        "/help — список команд"
    )


@dp.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer(
        "Я бот, созданный на Python с помощью aiogram!"
    )


@dp.message(F.text == "Группа")
async def cmd_group(message: Message):
    await message.answer("Твоя группа 71-1!")



@dp.message(F.text.lower() == "пока")
async def cmd_bye(message: Message):
    await message.answer("пока, До встречи 👋")



@dp.message(F.text)
async def echo(message: Message):
    await message.answer(message.text)


async def main():
    async with Bot(token=BOT_TOKEN) as bot:
        await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())