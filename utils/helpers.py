from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.user import user_main_ikb


async def start_anketa(message: types.Message, state: FSMContext):
    await message.answer(
        text="Ism sharifingizni kiriting"
    )
    await state.set_state(
        "start_anketa"
    )


async def start_text(message: types.Message):
    await message.answer(
        text="📚 <b>Ona tili fanidan Milliy sertifikat testlari</b>\n\n"
             "Assalomu alaykum! 👋\n"
             "Siz <b>Ona tili fanidan Milliy sertifikat imtihoniga tayyorgarlik ko‘rish</b> uchun "
             "mo‘ljallangan test botidasiz.\n\n"
             "🎯 <b>Bot orqali:</b>\n"
             "• Milliy sertifikat formatidagi testlarni ishlashingiz\n"
             "• O‘z bilim darajangizni sinab ko‘rishingiz\n"
             "• Test natijalaringizni ko‘rishingiz\n"
             "• O‘qituvchi sifatida o‘quvchilaringiz natijalarini kuzatishingiz mumkin.\n\n"
             "⭐ <b>Botning asosiy afzalliklari:</b>\n"
             "🌐 <b>Hamma uchun ochiq</b>\n"
             "Bot ma'lum bir o‘quv markaziga bog‘lanmagan. "
             "Istalgan o‘qituvchi va o‘quvchi undan foydalanishi mumkin.\n\n"
             "🚫 <b>Reklamasiz muhit</b>\n"
             "Sizga boshqa o‘qituvchilar, o‘quv markazlari yoki kurslarning reklamasi ko‘rsatilmaydi.\n"
             "👨‍🏫 <b>O‘qituvchilar uchun qulay</b>\n"
             "Har bir o‘qituvchiga o‘z o‘quvchilarining natijalarini alohida yuborish imkoniyati mavjud.\n"
             "📊 <b>Natijalarni nazorat qiling</b>\n"
             "O‘quvchingiz darajasini ko‘rib, uning bilimini tahlil qilishingiz mumkin.\n\n"
             "📖 <b>Maqsadimiz — tayyorgarlikni qulaylashtirish.</b>\n\n"
             "Testni boshlash uchun quyidagi menyudan foydalaning 👇",
        reply_markup=user_main_ikb()
    )
