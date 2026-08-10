from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def tch_main_ikb():
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton(
            text="Natijalarni olish", callback_data="tch_results"
        ),
        InlineKeyboardButton(
            text="Esse ball qo'yish", callback_data="tch_essay"
        )
    )
    return kb
