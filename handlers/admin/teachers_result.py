from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from magic_filter import F

from filters import IsBotAdminFilter
from loader import dp, appdb, rdb, bot
from utils.rash.uzbek.analyzer import generate_test_pdf


@dp.message_handler(IsBotAdminFilter(), F.text == "Ustozlarga natija", state="*")
async def hteacher_results(message: types.Message, state: FSMContext):
    await state.finish()
    teachers_str = str()

    teachers_db = await appdb.get_teachers()
    print(teachers_db)
    for t in teachers_db:
        teachers_str += f"{t['id']}. {t['first_name']} {t['last_name']}\n"

    await message.answer(
        text=f"Kerakli ustoz ID raqamini kiriting\n\n"
             f"{teachers_str}"
    )
    await state.set_state("teachers_result")


@dp.message_handler(state="teachers_result", content_types=['text'])
async def h_teachers_tch_id(message: types.Message, state: FSMContext):
    await state.update_data(
        teacher_id=int(message.text)
    )

    test_code_str = str()

    tests = await rdb.get_tests()

    for t in tests:
        test_code_str += f"{t['id']} | {t['subject']} | {t['test_code']}\n"

    await message.answer(
        text=f"Kerakli test id raqamini kiriting!\n\n"
             f"{test_code_str}"
    )
    await state.set_state("teachers_test_code")


@dp.message_handler(state="teachers_test_code", content_types=['text'])
async def h_teachers_finish(message: types.Message, state: FSMContext):
    data = await state.get_data()
    teacher_id = data.get("teacher_id")
    test_code_id = int(message.text)

    db_data = await appdb.get_tch_test_code(teacher_id, test_code_id)

    result = await rdb.get_result_by_tch_id(
        teacher_id=teacher_id, test_code_id=test_code_id
    )

    pdf_path = await generate_test_pdf(result, test_name="Test", test_code=db_data['test_code'])

    try:
        await bot.send_document(
            chat_id=db_data['telegram_id'],
            document=InputFile(pdf_path),
            caption=f"Natijalar tayyor!!!\n\n"
                    f"Test nomi: {db_data['test_code']}",
        )
    except Exception:
        await message.answer(
            text=f"Xatolik!!!\n\n"
                 f"Xabar {db_data['first_name']} {db_data['last_name']} ga yuborilmadi!"
        )
