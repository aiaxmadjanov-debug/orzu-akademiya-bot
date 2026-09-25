from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from keyboards.prices_menu import prices_menu
from keyboards.main_menu import main_menu


router = Router()


def price_service_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📝 Буюртма бериш")
            ],
            [
                KeyboardButton(text="☎️ Админ билан боғланиш")
            ],
            [
                KeyboardButton(text="⬅️ Нархлар")
            ],
            [
                KeyboardButton(text="🏠 Бош меню")
            ]
        ],
        resize_keyboard=True
    )


# =========================================================
# 💰 НАРХЛАР
# =========================================================

@router.message(F.text == "💰 Нархлар")
async def prices_menu_handler(message: Message):
    await message.answer(
        "💰 <b>ХИЗМАТЛАР НАРХЛАРИ</b>\n\n"
        "Хизмат нархи ишнинг ҳажми, мураккаблиги ва "
        "бажариш муддатига қараб белгиланади.\n\n"
        "📌 Аниқ нарх олиш учун:\n\n"
        "1️⃣ Хизмат турини танланг\n"
        "2️⃣ Мавзу ёки вазифани ёзинг\n"
        "3️⃣ Ҳажмини кўрсатинг\n"
        "4️⃣ Топшириш муддатини ёзинг\n\n"
        "Шундан сўнг мутахассисимиз сизга аниқ нархни айтади.\n\n"
        "Керакли бўлимни танланг 👇",
        reply_markup=prices_menu(),
        parse_mode="HTML"
    )


# =========================================================
# 💬 НАРХНИ АНИҚЛАШ
# =========================================================

@router.message(F.text == "💬 Нархни аниқлаш")
async def determine_price(message: Message):
    await message.answer(
        "💬 <b>НАРХНИ АНИҚЛАШ</b>\n\n"
        "Аниқ нарх ҳисоблаш учун қуйидаги маълумотларни юборинг:\n\n"
        "📚 <b>Хизмат:</b> қайси хизмат керак?\n"
        "📝 <b>Вазифа:</b> нима тайёрлаш керак?\n"
        "📑 <b>Ҳажм:</b> неча бет, слайд, видео ва ҳ.к.?\n"
        "⏰ <b>Муддат:</b> қачонга керак?\n\n"
        "Масалан:\n"
        "<i>Илмий мақола керак, 7 бет, 15 сентябргача.</i>\n\n"
        "Маълумотларни юборинг — администратор буюртмани "
        "кўриб чиқиб, сиз билан боғланади.",
        reply_markup=price_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# ☎️ АДМИН БИЛАН БОҒЛАНИШ
# =========================================================

@router.message(F.text == "☎️ Админ билан боғланиш")
async def admin_contact(message: Message):
    await message.answer(
        "☎️ <b>АДМИН БИЛАН БОҒЛАНИШ</b>\n\n"
        "👤 Администратор билан боғланиш учун:\n\n"
        "📩 <b>Telegram:</b> @UZB_ARZU\n\n"
        "Саволингиз ёки мурожаатингизни ёзиб қолдиринг.\n"
        "Имкони борича тез жавоб берамиз.\n\n"
        "<b>ORZU AKADEMIYA</b>\n"
        "Ғоядан — профессионал натижагача. ✨",
        reply_markup=price_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# ⬅️ НАРХЛАРГА ҚАЙТИШ
# =========================================================

@router.message(F.text == "⬅️ Нархлар")
async def back_to_prices(message: Message):
    await message.answer(
        "💰 <b>ХИЗМАТЛАР НАРХЛАРИ</b>\n\n"
        "Керакли бўлимни танланг 👇",
        reply_markup=prices_menu(),
        parse_mode="HTML"
    )


# =========================================================
# 🏠 БОШ МЕНЮ
# =========================================================

@router.message(F.text.in_({"🏠 Бош меню", "⬅️ Бош меню"}))
async def back_to_main(message: Message):
    await message.answer(
        "🏠 <b>Бош меню</b>\n\n"
        "Керакли бўлимни танланг 👇",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )