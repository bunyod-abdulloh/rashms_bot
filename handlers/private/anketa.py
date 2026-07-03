from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp


@dp.message_handler(state="start_anketa", content_types=['text'])
async def hstart_anketa_start(message: types.Message, state: FSMContext):
    pass
