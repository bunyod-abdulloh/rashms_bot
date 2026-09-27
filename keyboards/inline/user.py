from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from data.config import APP_URL


def user_main_ikb():
    kb = InlineKeyboardMarkup()
    url = f"{APP_URL}/pupil/home/"
    kb.add(
        InlineKeyboardButton(
            text="🚀 Test ishlash",
            web_app=WebAppInfo(url=url)
        ),
        InlineKeyboardButton(
            text="💰 To'lov",
            callback_data="paid"
        )
    )
    return kb


def send_check_img():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            text="✈️ Chekni yuborish",
            callback_data="check_money"
        ),
        InlineKeyboardButton(
            text="⬅️ Ortga",
            callback_data="back_main"
        )
    )
    return kb
