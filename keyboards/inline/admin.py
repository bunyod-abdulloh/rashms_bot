from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callbacks import adm_check_paid_cb, adm_sos_cb


def check_paid_ikb(telegram_id):
    kb = InlineKeyboardMarkup()

    kb.row(
        InlineKeyboardButton(
            text="Cancel",
            callback_data=adm_check_paid_cb.new(
                action="cancel", value=telegram_id
            )
        ),
        InlineKeyboardButton(
            text="Check",
            callback_data=adm_check_paid_cb.new(
                action="check_paid", value=telegram_id
            )
        )
    )
    return kb


def user_sos_ikb(telegram_id):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            text="Javob berish",
            callback_data=adm_sos_cb.new(
                action="adm-sos", value=telegram_id
            )
        )
    )
    return kb
