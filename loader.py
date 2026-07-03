from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from data import config
from data.config import REDIS_PASS
from utils.db_api.admin_db import AdminDB
from utils.db_api.core import Database
from utils.db_api.users_db import UsersDB
from utils.db_api.app_db import AppDB

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
#storage = RedisStorage2(
#    host='localhost',
#    port=6379,
#    db=5,
#    state_ttl=3600,
#    data_ttl=3600,
#    password=REDIS_PASS
#)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)
db = Database()
udb = UsersDB(db)
adb = AdminDB(db)
appdb = AppDB(db)