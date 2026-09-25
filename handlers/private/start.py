from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from loader import dp, udb, tchdb
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
            print(f"BU TEACHER ID: {teacher_id}")
            await state.update_data(
                teacher_id=teacher_id
            )
        else:
            await message.answer(
                text="Taklif havolasida xatolik bor! Ustozga murojaat qiling!"
            )
            return

    user = await udb.check_user(
        telegram_id=pupil_tg_id
    )

    if user:
        await start_text(
            message=message
        )
    else:
        await start_anketa(
            message=message, state=state
        )
