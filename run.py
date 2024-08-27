import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Replace with your bot's token
API_TOKEN = '7129515674:AAHjbQT8kKL0W5ik-7TP7BNWcJegOQ-WfP4'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
dp = Dispatcher()

# Handler for the /start command
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Hello! How can I assist you today?")

# Handler for the /help command
@dp.message(Command("help"))
async def send_help(message: types.Message):
    await message.reply("You can send any message, and I'll reply to it!")

# Handler for echoing messages
@dp.message()
async def echo(message: types.Message):
    await message.answer(f"You said: {message.text}")

async def main():
    bot = Bot(token=API_TOKEN)

    # Start polling
    await dp.start_polling(bot)

# Run the bot
if __name__ == '__main__':
    asyncio.run(main())


# Start polling to handle incoming messages
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
