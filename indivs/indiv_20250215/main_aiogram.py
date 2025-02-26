import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart

TOKEN = "7614125102:AAHOCQgrHb6etX3rwp5ZvWgh1JObdqc3CPk"

bot = Bot(token=TOKEN)


dp = Dispatcher()

@dp.message(CommandStart())
async def start_command_handler(message):
    print(f"User {message.from_user.id} started the bot")
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"You text me with command!"
    )




async def main():
    await dp.start_polling(bot)

asyncio.run(main())
