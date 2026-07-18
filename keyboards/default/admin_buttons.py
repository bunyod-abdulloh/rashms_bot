from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo
)

from data.config import ADMIN_PANEL_URL

admin_main_btns = ReplyKeyboardMarkup(resize_keyboard=True)

admin_main_btns.add(
    KeyboardButton(
        text="🌐 Web panel",
        web_app=WebAppInfo(url=ADMIN_PANEL_URL)
    )
)

admin_main_btns.row("😊 Foydalanuvchilar soni")
admin_main_btns.row("✅ Oddiy post yuborish")
admin_main_btns.row("🎞 Mediagroup post yuborish")
admin_main_btns.row("Deep Link")
admin_main_btns.row("Umumiy natija")
admin_main_btns.row("Ustozlarga natija")
admin_main_btns.row("🏡 Bosh sahifa")
