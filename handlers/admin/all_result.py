from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters import IsBotAdminFilter
from loader import dp, rdb
from utils.rash.all_result import analyze_results


@dp.message_handler(IsBotAdminFilter(), F.text == "Umumiy natija", state="*")
async def hall_results(message: types.Message, state: FSMContext):
    await state.finish()
    tests = await rdb.get_tests()

    text = str()

    for t in tests:
        text += f"{t['id']} | {t['subject']} | {t['test_code']}\n"

    await message.answer(
        text=f"{text}\nKerakli test id raqamini kiriting!"
    )
    await state.set_state("all_result")


@dp.message_handler(state="all_result", content_types=['text'])
async def h_all_results_process(message: types.Message, state: FSMContext):
    test_code_id = int(message.text)

    await analyze_results(test_code_id)
