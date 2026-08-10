from math import ceil

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callbacks import tch_tests_cb


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


ITEMS_PER_PAGE = 10


def tch_tests_keyboard(tests, page=1):
    total_pages = ceil(len(tests) / ITEMS_PER_PAGE)

    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    keyboard = InlineKeyboardMarkup(row_width=1)

    for c in tests[start:end]:
        keyboard.add(
            InlineKeyboardButton(
                c["test_code"],
                callback_data=tch_tests_cb.new(
                    action="tch_tst", value=c["id"]
                )
            )
        )

    nav = []

    if page == 1:
        nav.append(
            InlineKeyboardButton(
                text="⬅️ Ortga",
                callback_data="tch_back"
            )
        )
    else:
        if page > 1:
            nav.append(
                InlineKeyboardButton("⬅️", callback_data=tch_tests_cb.new(
                    action="prev", value=page - 1
                ))  # f"page:{page-1}"
            )

        nav.append(
            InlineKeyboardButton(
                f"{page}/{total_pages}",
                callback_data="ignore"
            )
        )

        if page < total_pages:
            nav.append(
                InlineKeyboardButton("➡️", callback_data=tch_tests_cb.new(
                    action="next", value=page + 1
                ))  # f"page:{page+1}"
            )

    keyboard.row(*nav)

    return keyboard
