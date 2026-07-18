import re

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, appdb
from utils.helpers import start_text


@dp.message_handler(state="start_anketa", content_types=['text'])
async def hstart_anketa_start(message: types.Message, state: FSMContext):
    pupil_fullname = message.text

    # Lotin harflari, bo‘sh joy, apostrof turlari
    pattern = r"[A-Za-zʼ'ʻ]+( [A-Za-zʼ'ʻ]+){0,3}"

    if not re.fullmatch(pattern, pupil_fullname):
        await message.answer("Iltimos, faqat lotincha harf va bitta probel bilan kiriting!")
        return

    if len(pupil_fullname) > 30:
        await message.answer(
            text="Iltimos, ism sharifingizni kiriting"
        )
        return
    data = await state.get_data()

    teacher_id = data.get('teacher_id')
    pupil_tg_id = int(message.from_user.id)

    await appdb.add_pupil(
        telegram_id=pupil_tg_id, full_name=pupil_fullname, teacher_id=teacher_id
    )
    await state.finish()

    await start_text(
        message=message
    )
