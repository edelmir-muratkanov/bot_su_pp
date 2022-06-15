from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.contrib.fsm_storage.mongo import MongoStorage


from data.config import BOT_TOKEN, MONGO_URL


storage = MemoryStorage()
# storage = MongoStorage(uri=MONGO_URL)
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=storage)
