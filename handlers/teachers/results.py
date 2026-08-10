from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from loader import dp, tchdb


@dp.callback_query_handler(F.data == "tch_results", state="*")
async def h_tch_results_start(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    tests = await tchdb.get_teacher_tests(int(call.from_user.id))

    txt = "Test nomi va test o'tkazilgan sanalar\n\n"

    for t in tests:
        txt += f"{t['test_code']} | {t['created_at']}\n"

    await call.message.edit_text(
        text=f"{txt}\n"
             f"Kerakli testni tanlang",
        reply_markup=None
    )
