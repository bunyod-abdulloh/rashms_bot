from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline.callbacks import adm_check_paid_cb
from keyboards.inline.user import user_main_ikb
from loader import dp, udb, bot


@dp.callback_query_handler(adm_check_paid_cb.filter(action="check_paid"), state="*")
async def h_check_adm_paid(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.finish()

    tg_id = callback_data.get("value")

    await udb.set_paid_true(tg_id=int(tg_id))

    await call.message.delete()
    await call.message.answer(
        text=f"<code>{tg_id}</code>\n\n"
             f"Foydalanuvchiga test yoqildi!"
    )

    try:

        await bot.send_message(
            chat_id=tg_id,
            text="To'lovingiz tasdiqlandi! Test javoblarini kiritishingiz mumkin!",
            reply_markup=user_main_ikb()
        )
    except Exception as e:
        await call.message.answer(
            text=f"Xabar foydalanuvchiga yuborilmadi! Sabab:\n\n{e}"
        )


@dp.callback_query_handler(adm_check_paid_cb.filter(action="cancel"))
async def h_check_cancel_start(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.finish()

    tg_id = callback_data.get("value")

    await state.update_data(telegram_id=int(tg_id))

    await call.message.delete()
    await call.message.answer(
        text="Rad etilishi sababini kiriting"
    )
    await state.set_state("cancel_check_paid")


@dp.message_handler(state="cancel_check_paid", content_types=["text"])
async def h_cancel_check_process(message: Message, state: FSMContext):
    data = await state.get_data()
    tg_id = data.get("telegram_id")

    txt = message.text

    try:
        await bot.send_message(
            chat_id=tg_id,
            text=f"To'lov rad qilindi! Sabab:\n\n{txt}"
        )
        await message.answer(
            text="Xabar foydalanuvchiga yuborildi!"
        )

    except Exception as e:
        await message.answer(
            text=f"Xabar foydalanuvchiga yuborilmadi! Sabab:\n\n{e}"
        )

    await state.finish()
