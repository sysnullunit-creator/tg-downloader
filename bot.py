import asyncio
import os
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

# Загружаем переменные из .env
load_dotenv()

# Проверяем, что токен есть
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env")

# Включаем логирование, чтобы видеть, что происходит
logging.basicConfig(level=logging.INFO)

# Создаем диспетчер — он будет распределять сообщения по обработчикам
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n"
        f"Я пока ничего не умею, но скоро научусь скачивать видео."
    )


async def main():
    bot = Bot(token=BOT_TOKEN)
    print("Бот запущен. Нажми Ctrl+C для остановки.")
    # start_polling запускает бесконечный цикл получения обновлений
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())