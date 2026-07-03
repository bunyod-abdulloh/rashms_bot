from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from data.config import ADMINS
from loader import dp, appdb, bot


@dp.message_handler(F.text == "Deep Link", state="*", user_id=ADMINS[0])
async def hdeep_link_start(message: types.Message, state: FSMContext):
    await state.finish()

    teachers = await appdb.get_teachers()

    text = str()

    for t in teachers:
        text += f"{t['id']}. {t['first_name']} {t['last_name']}\n"

    await message.answer(
        text=f"{text}\n"
             f"Taklif havolasi yubormoqchi bo'lgan ustoz ID raqamini kiriting"
    )
    await state.set_state(
        "deep_link_process"
    )


@dp.message_handler(state="deep_link_process", content_types=['text'])
async def hdeep_link_process(message: types.Message, state: FSMContext):
    teacher_id = int(message.text)

    teacher = await appdb.get_teacher_by_id(
        teacher_id=teacher_id
    )

    bot_username = (await bot.get_me()).username
    invite_link = f"https://t.me/{bot_username}?start={teacher['telegram_id']}"

    share_text = (
        f"\nUstoz: {teacher['first_name']} {teacher['last_name']}\n\n"
        f"Taklif havolasi:\n\n{invite_link}"
    )

    try:
        await bot.send_message(
            chat_id=teacher['telegram_id'],
            text=share_text,
        )
        await message.answer(
            text=share_text
        )
    except Exception as e:
        await message.answer(
            text=f"XATOLIK: {e}"
        )

    await state.finish()
