from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters import IsBotAdminFilter
from loader import dp


@dp.message_handler(IsBotAdminFilter(), F.text == "Ustozlarga natija", state="*")
async def hteacher_results(message: types.Message, state: FSMContext):
    await state.finish()
