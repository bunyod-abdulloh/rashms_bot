from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from loader import dp, appdb
from utils.helpers import start_anketa, start_text


@dp.message_handler(CommandStart(), state="*")
async def handle_start(message: types.Message, state: FSMContext):
    await state.finish()
    deep_link = message.get_args()

    pupil_tg_id = int(message.from_user.id)

    if deep_link:
        await state.update_data(
            teacher_tg_id=int(deep_link)
        )

    user = await appdb.check_user(
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
