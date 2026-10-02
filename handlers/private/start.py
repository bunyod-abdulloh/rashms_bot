from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from data.config import CHANNEL
from loader import dp, udb, tchdb, bot
from utils.helpers import start_anketa, start_text


@dp.message_handler(CommandStart(), state="*")
async def handle_start(message: types.Message, state: FSMContext):
    await state.finish()
    deep_link = message.get_args()

    pupil_tg_id = int(message.from_user.id)

    if deep_link:
        teacher = await tchdb.check_teacher(
        teacher_telegram_id=int(deep_link)
        )
        if teacher:
            teacher_id = await tchdb.get_teacher_by_tg_id(
                teacher_tg_id=int(deep_link)
            )
            await state.update_data(
                teacher_id=teacher_id
            )
        else:
            await message.answer(
                text="Taklif havolasida xatolik bor! Ustozga murojaat qiling!"
            )
            return None

    user = await udb.check_user(
        telegram_id=pupil_tg_id
    )

    member = await bot.get_chat_member(
        chat_id=CHANNEL, user_id=pupil_tg_id
    )

    allowed_statuses = ["member", "creator", "administrator"]

    if member.status not in allowed_statuses:
        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton(
                text="✅ Obunani tekshirish",
                callback_data="subscribed"
            )
        )

        return await message.answer(
            text="Siz kanalimizga a'zo bo'lmadingiz! Botdan foydalanish uchun quyidagi kanalimizga obuna bo'lishingiz "
                 "lozim!\n\n"
                 "https://t.me/onatilirashms\n\n"
                 "Agar obuna bo'lgan bo'lsangiz <b>Obunani tekshirish</b> tugmasini bosing",
            reply_markup=kb
        )

    if user:
        await start_text(
            event=message
        )
        return None
    else:
        await start_anketa(
            message=message, state=state
        )
        return None
