from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("IP")
REDIS_PASS = env.str("REDIS_PASS")
ADMIN_PANEL_URL = env.str("ADMIN_PANEL_URL")

DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")
DB_PORT = env.str("DB_PORT")

WEB_APP_URL = env.str("WEB_APP_URL")

APP_URL = env.str("APP_URL")

WEBHOOK_PATH = env.str("WEBHOOK_PATH")
WEBAPP_HOST = env.str("WEBAPP_HOST")
WEBAPP_PORT = env.int("WEBAPP_PORT")
