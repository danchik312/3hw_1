from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config

storage = MemoryStorage()
TOKEN = config('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher()
ADMIN_ID=config('ADMIN_ID')
MEDIA_PATH=config('MEDIA_PATH')
