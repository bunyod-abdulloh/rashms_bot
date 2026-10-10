import re

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from magic_filter import F

from loader import dp, udb
from utils.helpers import start_text
from utils.txts import FULL_NAME_TEXT


@dp.callback_query_handler(F.data == "edit_profile", state="*")
async def h_edit_profile_start(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(
        text=FULL_NAME_TEXT
    )
    await state.set_state("edit_full_name")


@dp.message_handler(state="edit_full_name", content_types=["text"])
async def h_edit_full_name(message: Message, state: FSMContext):
    full_name = message.text.strip()

    pattern = r"[A-Za-zʼ'ʻ]+( [A-Za-zʼ'ʻ]+){0,3}"

    if not re.fullmatch(pattern, full_name):
        await message.answer("Iltimos, faqat lotincha harf va bitta probel bilan kiriting!")
        return

    if len(full_name) > 30:
        await message.answer(
            text=FULL_NAME_TEXT
        )
        return

    await udb.set_user_full_name(
        full_name=full_name, telegram_id=int(message.from_user.id)
    )
    await message.answer(
        text="✅ Ism sharif o'zgartirildi!"
    )
    await start_text(
        event=message
    )
    await state.finish()
