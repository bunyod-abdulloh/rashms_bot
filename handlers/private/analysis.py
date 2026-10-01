from datetime import datetime, timedelta

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from magic_filter import F

from data.config import VOICE_CHAT_GROUP
from loader import dp, bot


@dp.callback_query_handler(F.data == "analysis", state="*")
async def h_analysis_start(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.answer(
        text="Bo'lim hozircha faol emas!",
        show_alert=True
    )
    return
    invite_link = await bot.create_chat_invite_link(
        chat_id=VOICE_CHAT_GROUP,
        member_limit=1,
        expire_date=datetime.now() + timedelta(hours=10),
    )
