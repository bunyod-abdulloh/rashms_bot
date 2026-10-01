import asyncio
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from data.config import ADMINS
from filters import IsBotAdminFilter
from loader import dp, rdb, bot
from utils.rash.uzbek.analyzer import analyze_results


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


RUNNING: set[int] = set()  # bir vaqtda bitta test ikki marta hisoblanmasligi uchun


@dp.message_handler(state="all_result", content_types=["text"])
async def h_all_results_process(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("⏳ Natijalar hisoblanmoqda...")
    asyncio.create_task(run_analysis(int(message.text)))  # handler darhol tugaydi


async def run_analysis(test_code_id: int):
    if test_code_id in RUNNING:
        return
    RUNNING.add(test_code_id)
    try:
        await analyze_results(test_code_id)
    except Exception:
        logging.exception("analyze_results failed")
        await bot.send_message(ADMINS[0], "⚠️ Hisoblashda xatolik, loglarni tekshiring")
    finally:
        RUNNING.discard(test_code_id)
