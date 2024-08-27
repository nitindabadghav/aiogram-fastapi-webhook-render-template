from fastapi import FastAPI, Request
import time
import logging
import os
from contextlib import asynccontextmanager


from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, Update
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from services.helpers import (
    get_response)
import os
from dotenv import load_dotenv
from services.app_logging.logger import Logger
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS

# ============= INITIALIZER ===============================

TOKEN = "7129515674:AAEueiEQwLKF-GAIEmG0MyCBXshmhz-umMY"

WEBHOOK_PATH = f"/webhook"
# RENDER_WEB_SERVICE_NAME = "aec9-223-233-84-28.ngrok-free.app"
RENDER_WEB_SERVICE_NAME = "maalikatelbot"
# WEBHOOK_URL = "https://" + RENDER_WEB_SERVICE_NAME + ".onrender.com" + WEBHOOK_PATH
WEBHOOK_URL = "https://" + RENDER_WEB_SERVICE_NAME + ".onrender.com" + WEBHOOK_PATH

logging.basicConfig(filemode='a', level=logging.INFO)

os.environ["GOOGLE_API_KEY"] = "AIzaSyBPNlxK0jsb9Et0bjViu4zOuy8d13-50P8"

embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")


llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.9,
)

prompt_template = """ You are an expert in Bhavishya Maalika.
  Read the context carefully and Answer the question as detailed as possible from the provided context, make sure to provide all the details\n\n
  Context:\n {context}?\n
  Question: \n{question}\n

  Answer:
"""

prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)
# logger.info(llm)
new_db = FAISS.load_local("data/faiss_index", embeddings, allow_dangerous_deserialization=True)

# ================================================================================================================


bot = Bot(token=TOKEN)
dp = Dispatcher()
app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    print("-------------------------------Info------------------------------")
    webhook_info = await bot.get_webhook_info()

    print(webhook_info)
    print("-------------------------------Info------------------------------")
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True
        )
    
    yield  # This point is where the app runs

    # Shutdown code
    await bot.get_session().close()


@dp.message(CommandStart())
async def start_handler(message: Message):
    bot_message = """
    Welcome to the world of Bhavishya Maalika. Ask any questions related to Bhavishya Maalika and I will try to answer them as precisely as possible.\n You can start by asking 'What is Bhavishya Maalika all about', 'Who wrote Bhavishya Maalika" etc.
    """
    await message.reply(f"{bot_message}")

@dp.message()
async def main_handler(message: Message):
    try:
        # user_id = message.from_user.id
        # user_full_name = message.from_user.full_name
        # logging.info(f'Main: {user_id} {user_full_name} {time.asctime()}. Message: {message}')
        question = message.text
        response = get_response(chain, new_db, question)
        await message.reply(response)
    except:
        logging.info(f'Main: Error in main_handler')
        await message.reply("Something went wrong...")    

@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request):
    print("................................................................in here11111111111111111111111111111111")
    data = await request.json()
    chat_id = data['message']['chat']['id']
    text = data['message']['text']
    print(f"=============================================== {text}")
    update = Update(**await request.json())
    await dp.feed_webhook_update(bot,update=update)
    return text
