from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline.user import back_ikb
from loader import dp


@dp.callback_query_handler(F.data == "delete-answers", state="*")
async def h_delete_answers_start(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(
        text="O'chirilishi kerak bo'lgan test kodini kiriting",
        reply_markup=back_ikb()
    )
    await state.set_state("delete-answers")


@dp.message_handler(state="delete-answers", content_types=["text"])
async def h_delete_answers_process(message: Message, state: FSMContext):
    test_code = message.text.strip().lower()

    test_code_ = await
