from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from data.config import CHANNEL
from loader import dp, bot
from utils.helpers import start_text


@dp.callback_query_handler(F.data == "subscribe", state="*")
async def h_subscribe_start(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    user_id = call.from_user.id

    member = await bot.get_chat_member(
        chat_id=CHANNEL, user_id=user_id
    )

    allowed_statuses = ["member", "creator", "administrator"]

    if member.status not in allowed_statuses:
        return await call.answer(
            text="Siz kanalimizga a'zo bo'lmadingiz! Botdan foydalanish uchun kanalimizga a'zo bo'lishingiz lozim!",
            show_alert=True
        )

    await start_text(
        event=call
    )
    return None
