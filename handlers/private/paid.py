from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from data.config import ADMINS
from keyboards.inline.admin import check_paid_ikb
from keyboards.inline.user import send_check_img
from loader import dp, bot


@dp.message_handler(F.data == "paid", state="*")
async def h_paid_start(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.edit_text(
        text="Quyidagi karta raqamiga 5000 so'm pul o'tkazib chek rasmini yuboring. To'lov tasdiqlanganidan "
             "so'ng test Siz uchun ochiladi.\n\n"
             "<code>1234123412341234</code>",
        reply_markup=send_check_img()
    )


@dp.callback_query_handler(F.data == "check_money", state="*")
async def h_check_money_start(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(
        text="Chek rasmini yuboring"
    )
    await state.set_state("check_paid")


@dp.message_handler(state="check_paid", content_types=["photo"])
async def h_check_paid_process(message: types.Message, state: FSMContext):
    await message.answer(
        text="Chek qabul qilindi! To'lov tasdiqlanganidan so'ng Sizga xabar yuboriladi!"
    )
    await state.finish()

    photo_id = message.photo[-1].file_id

    await bot.send_photo(
        chat_id=ADMINS[0],
        photo=photo_id,
        caption="Yangi to'lov qabul qilindi!",
        reply_markup=check_paid_ikb(
            telegram_id=message.from_user.id
        )
    )
