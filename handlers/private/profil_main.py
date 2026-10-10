from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from magic_filter import F

from keyboards.inline.user import edit_profile_ikb
from loader import dp, udb


@dp.callback_query_handler(F.data == "profile", state="*")
async def h_profile_main(call: CallbackQuery, state: FSMContext):
    await state.finish()
    tg_id = int(call.from_user.id)

    user = await udb.get_user(telegram_id=tg_id)

    if user:
        await call.message.edit_text(
            text=f"Ism - sharifingiz: {user['full_name']}\n\n"
                 f"O'zgartirmoqchi bo'lsangiz 📝 O'zgartirish tugmasini bosing",
            reply_markup=edit_profile_ikb()
        )
    else:
        await call.message.edit_text(
            text="Botda ro'yxatdan o'tishda xatolik bo'lgan! Iltimos qayta /start tugmasini bosib ro'yxatdan o'ting"
        )
