from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from magic_filter import F

from keyboards.inline.user import user_main_ikb, back_ikb
from loader import dp


@dp.callback_query_handler(F.data == "rules", state="*")
async def h_rules_start(call: CallbackQuery, state: FSMContext):
    await state.finish()

    text = ("<b>⚠️ Javoblaringiz to‘g‘ri chiqishi uchun quyidagi qoidalarga amal qiling:</b>\n\n"
            "🔹 <b>Yozma qismda matnlarni KATTA HARFLARDA kiriting</b>)\n\n"
            "🔹 <b>Qo‘shtirnoqni quyidagi ko‘rinishda kiriting: "
            "\"____\"</b>\n\n"
            "🔹 <b>Chiziqchalarni bo‘sh joy tashlamasdan yozing."
            "Masalan:</b> <code>kamdan-kam</code>\n\n>"
            "<b>Tutuq belgisi ’, O‘, G‘ uchun ' belgisini ishlating</b>\n\n" 
            "🔹 Esse ballni o'zingiz kiriting")
    await call.message.edit_text(
        text=text,
        reply_markup=back_ikb()
    )


@dp.callback_query_handler(F.data == "back_main", state="*")
async def h_back_main(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(
        text="Bosh sahifa",
        reply_markup=user_main_ikb()
    )
