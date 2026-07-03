from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.user import user_main_ikb


async def start_anketa(message: types.Message, state: FSMContext):
    await message.answer(
        text="Ism sharifingizni kiriting"
    )
    await state.set_state(
        "start_anketa"
    )


async def start_text(message: types.Message):
    await message.answer(
        text="Assalomu alaykum! Rash MS botimizga xush kelibsiz!",
        reply_markup=user_main_ikb()
    )
