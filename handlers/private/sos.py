from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from data.config import ADMINS
from keyboards.inline.admin import user_sos_ikb
from loader import dp, bot


@dp.callback_query_handler(F.data == "sos", state="*")
async def h_sos_start(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(
        text="Matnli yoki rasm shaklida savollaringizni yuborishingiz mumkin! Rasmga qo'shimcha matnli savolingiz "
             "bo'lsa rasm bilan qo'shib yuboring. \n\nSavolingizni yuboring"
    )
    await state.set_state("sos-user")


@dp.message_handler(state="sos-user", content_types=["text", "photo"])
async def h_sos_process(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    hlink = f"<code>{telegram_id}</code>\n\n"

    if message.content_type == "photo":
        await bot.send_photo(
            chat_id=ADMINS[0],
            photo=message.photo[-1].file_id,
            caption=hlink + message.caption,
            reply_markup=user_sos_ikb(
                telegram_id=telegram_id
            )
        )
    elif message.content_type == "text":
        await bot.send_message(
            chat_id=ADMINS[0],
            text=hlink + message.text,
            reply_markup=user_sos_ikb(
                telegram_id=telegram_id
            )
        )

    await message.answer(
        text="Xabaringiz adminga yuborildi! Tez orada javob qaytarishga harakat qilamiz!"
    )
    await state.finish()
