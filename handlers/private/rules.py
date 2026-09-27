from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from magic_filter import F

from keyboards.inline.user import back_ikb, user_main_ikb
from loader import dp


@dp.callback_query_handler(F.data == "rules", state="*")
async def h_rules_start(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(
        text='Javoblaringiz to\'g\'ri chiqishi uchun quyidagi qoidalarga amal qiling:\n\n'
             '- yozma qismda matnlarni katta harflarda kiriting;\n'
             '- qo\'shtirnoqni "____" ko\'rinishida kiriting;\n'
             '- chiziqchalarni bo\'sh joy tashlamasdan yozing (masalan, "kamdan-kam");\n',
        reply_markup=back_ikb()
    )


@dp.callback_query_handler(F.data == "back_main", state="*")
async def h_back_main(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(
        text="Bosh sahifa",
        reply_markup=user_main_ikb()
    )
