from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from data.config import APP_URL


def user_main_ikb():
    kb = InlineKeyboardMarkup()
    url = f"{APP_URL}/pupil/home/"
    kb.add(
        InlineKeyboardButton(
            text="🛍 Test ishlash",
            web_app=WebAppInfo(url=url)
        )
    )
    return kb
