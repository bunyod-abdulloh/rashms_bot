from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.teachers import tch_main_ikb
from loader import dp, tchdb


@dp.message_handler(commands=['teachers'], state="*")
async def h_teachers_main(message: types.Message, state: FSMContext):
    await state.finish()

    teacher = await tchdb.check_teacher(int(message.from_user.id))

    if teacher:
        await message.answer(
            text="Kerakli bo'limni tanlang",
            reply_markup=tch_main_ikb()
        )
        return
    else:
        await message.answer(
            text="Siz ustozlar ro'yxatida yo'q ekansiz! Iltimos, bot adminiga murojaat qiling"
        )
