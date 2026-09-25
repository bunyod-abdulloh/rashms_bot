from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from magic_filter import F

from filters import IsBotAdminFilter
from loader import dp, rdb, bot
from utils.rash.uzbek.analyzer import generate_test_pdf


@dp.message_handler(IsBotAdminFilter(), F.text == "Ustozlarga natija", state="*")
async def hteacher_results(message: types.Message, state: FSMContext):
    await state.finish()
    test_str = str()

    # tests = await rdb.get_teachers_test()
    tests = await rdb.sample_teach()

    for t in tests:
        test_str += f"ID: {t['test_id']} SUBJECT: {t['subject']} TEST_NAME: {t['test_name']}\n"

    await message.answer(
        text=f"Kerakli test ID raqamini kiriting\n\n"
             f"{test_str}"
    )
    await state.set_state("teachers_result")


@dp.message_handler(state="teachers_result", content_types=['text'])
async def h_teachers_tch_id(message: types.Message, state: FSMContext):
    await state.update_data(
        teacher_id=int(message.text)
    )
    test_id = int(message.text.strip())

    teachers = await rdb.get_teachers_rr(test_id=test_id)

    for t in teachers:
        result = await rdb.get_result_by_tch_id(
            teacher_id=t['teacher_id'], test_code_id=t['test_id']
        )

        pdf_path = await generate_test_pdf(result, test_name="Test", test_code=t['test_code'])

        try:
            await bot.send_document(
                chat_id=t['telegram_id'],
                document=InputFile(pdf_path),
                caption=f"Natijalar tayyor!!!\n\n"
                        f"Test nomi: {t['test_code']}",
            )
            await message.answer(
                text=f"Xabar ustoz {t['first_name']} {t['last_name']} ga yuborildi!\n\n"
            )
        except Exception:
            await message.answer(
                text=f"Xatolik!!!\n\n"
                     f"Xabar {t['first_name']} {t['last_name']} ga yuborilmadi!"
            )
