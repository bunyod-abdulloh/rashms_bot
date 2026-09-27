from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from data.config import APP_URL


def user_main_ikb():
    kb = InlineKeyboardMarkup(row_width=1)
    url = f"{APP_URL}/pupil/home/"
    kb.add(
        InlineKeyboardButton(
            text="🚀 Test ishlash",
            web_app=WebAppInfo(url=url)
        ),
        InlineKeyboardButton(
            text="💰 To'lov",
            callback_data="paid"
        ),
        InlineKeyboardButton(
            text="✍️ Adminga murojaat",
            callback_data="sos"
        )
    )
    return kb


def send_check_img():
    kb = InlineKeyboardMarkup(row_width=1)
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
