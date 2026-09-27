from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline.callbacks import adm_sos_cb
from loader import dp, bot


@dp.callback_query_handler(adm_sos_cb.filter(action="adm-sos"), state="*")
async def h_adm_sos_start(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.finish()
    sos_tg_id = callback_data.get("value")

    await call.message.answer(
        text="Javobingizni kiriting"
    )
    await state.update_data(
        sos_tg_id=sos_tg_id
    )
    await state.set_state("adm-sos")


@dp.message_handler(state="adm-sos", content_types=['text'])
async def h_adm_sos_process(message: Message, state: FSMContext):
    data = await state.get_data()

    sos_tg_id = data.get("sos_tg_id")
    txt = message.text

    try:
        await bot.send_message(
            chat_id=sos_tg_id,
            text=f"Savolingizga admin javobi:\n\n{txt}"
        )
        await message.answer(
            text="Xabaringiz foydalanuvchiga yuborildi!"
        )
    except Exception as e:
        await message.answer(
            text=f"Xabar foydalanuvchiga yuborilmadi! Sabab:\n\n"
                 f"{e}"
        )
    await state.finish()
