from fastapi import FastAPI
import time
import logging
import os
from contextlib import asynccontextmanager


from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command


TOKEN = "7129515674:AAHjbQT8kKL0W5ik-7TP7BNWcJegOQ-WfP4"

WEBHOOK_PATH = f"/bot/{TOKEN}"
RENDER_WEB_SERVICE_NAME = "maalikatelbot"
WEBHOOK_URL = "https://" + RENDER_WEB_SERVICE_NAME + ".onrender.com" + WEBHOOK_PATH

logging.basicConfig(filemode='a', level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
dp.start_polling()
app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )
    
    yield  # This point is where the app runs

    # Shutdown code
    await bot.get_session().close()


@dp.message(Command=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'Start: {user_id} {user_full_name} {time.asctime()}. Message: {message}')
    await message.reply(f"Hello, {user_full_name}!")

@dp.message()
async def main_handler(message: types.Message):
    try:
        user_id = message.from_user.id
        user_full_name = message.from_user.full_name
        logging.info(f'Main: {user_id} {user_full_name} {time.asctime()}. Message: {message}')
        await message.reply("Hello world!")
    except:
        logging.info(f'Main: {user_id} {user_full_name} {time.asctime()}. Message: {message}. Error in main_handler')
        await message.reply("Something went wrong...")    

@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)


@app.get("/")
def main_web_handler():
    return "Everything ok!"