import middlewares, filters, handlers

from aiohttp import web
from aiogram.dispatcher.webhook import get_new_configured_app

from data.config import WEB_APP_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_SECRET
from loader import dp, bot, db
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

WEBHOOK_URL = f"{WEB_APP_URL}{WEBHOOK_PATH}"


async def on_startup(dispatcher):
    try:
        await on_startup_notify(dispatcher)
        await set_default_commands(dispatcher)
        print("✅ Notify done")
    except Exception as e:
        print(f"❌ Notify error: {e}")

    try:
        await db.create()
        await db.create_tables()
        print("✅ DB ready")
    except Exception as e:
        print(f"❌ DB error: {e}")

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        # secret_token endi Telegram'ga ham yuborilyapti —
        # shu bilan Telegram har bir so'rovga shu tokenni header orqali qo'shadi
        await bot.set_webhook(WEBHOOK_URL, secret_token=WEBHOOK_SECRET)
        print(f"✅ Webhook set: {WEBHOOK_URL}")
    except Exception as e:
        print(f"❌ Webhook error: {e}")


async def on_shutdown(dispatcher):
    try:
        await bot.delete_webhook()
    finally:
        await bot.session.close()


@web.middleware
async def verify_telegram_secret(request: web.Request, handler):
    # Faqat webhook manziliga kelayotgan so'rovlarni tekshiramiz
    if request.path == WEBHOOK_PATH:
        token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if token != WEBHOOK_SECRET:
            return web.Response(status=403, text="Forbidden")
    return await handler(request)


def main():
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_PATH)
    app.middlewares.append(verify_telegram_secret)

    # on_startup/on_shutdown'ni aiohttp lifecycle hook'lariga ulaymiz
    app.on_startup.append(lambda _: on_startup(dp))
    app.on_shutdown.append(lambda _: on_shutdown(dp))

    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)


if __name__ == "__main__":
    main()
