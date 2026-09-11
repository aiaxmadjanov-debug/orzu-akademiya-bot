from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from keyboards.promotions_menu import promotions_menu
from keyboards.main_menu import main_menu


router = Router()


def promotion_service_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📝 Буюртма бериш")
            ],
            [
                KeyboardButton(text="⬅️ Акциялар")
            ],
            [
                KeyboardButton(text="🏠 Бош меню")
            ]
        ],
        resize_keyboard=True
    )


@router.message(F.text == "🔥 Акциялар")
async def promotions_menu_handler(message: Message):
    await message.answer(
        "🔥 <b>ORZU AKADEMIYA МАХСУС АКЦИЯЛАРИ!</b>\n\n"
        "Сиз учун махсус таклифлар ва бонуслар.\n\n"
        "🔥 Чегирмалар\n"
        "🎁 Бонус хизматлар\n"
        "⏰ Муддатли таклифлар\n"
        "📚 Китоб нашри учун акциялар\n"
        "🎓 Илмий хизматлар акциялари\n\n"
        "📌 Акциялар тез-тез янгиланади.\n\n"
        "Керакли бўлимни танланг 👇",
        reply_markup=promotions_menu(),
        parse_mode="HTML"
    )


@router.message(F.text == "🔥 Жорий акциялар")
async def current_promotions(message: Message):
    await message.answer(
        "🔥 <b>ЖОРИЙ АКЦИЯЛАР</b>\n\n"
        "Ҳозирги махсус таклифлар:\n\n"
        "🎁 <b>Акциялар тез орада янгиланади.</b>\n\n"
        "Янги акциялар, чегирмалар ва бонуслар "
        "шу бўлимда эълон қилинади.\n\n"
        "📌 Аниқ нарх ва шартлар учун администратор билан боғланинг.",
        reply_markup=promotion_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "🎁 Бонуслар")
async def bonuses(message: Message):
    await message.answer(
        "🎁 <b>БОНУСЛАР</b>\n\n"
        "Айрим хизматлар учун махсус бонуслар тақдим этилади.\n\n"
        "☑️ Қўшимча хизматлар\n"
        "☑️ Бонус материаллар\n"
        "☑️ Махсус таклифлар\n\n"
        "📌 Бонуслар акция шартларига қараб ўзгариши мумкин.",
        reply_markup=promotion_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "⏰ Муддатли таклифлар")
async def limited_offers(message: Message):
    await message.answer(
        "⏰ <b>МУДДАТЛИ ТАКЛИФЛАР</b>\n\n"
        "Чекланган муддат давомида амал қиладиган махсус таклифлар.\n\n"
        "🔥 Чегирмалар\n"
        "🎁 Бонуслар\n"
        "📚 Нашриёт хизматлари\n"
        "🎓 Илмий хизматлар\n"
        "🎨 Дизайн ва медиа\n\n"
        "📌 Таклифлар муддати акцияга қараб белгиланади.",
        reply_markup=promotion_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "📚 Китоб нашри акциялари")
async def book_promotions(message: Message):
    await message.answer(
        "📚 <b>КИТОБ НАШРИ АКЦИЯЛАРИ</b>\n\n"
        "Китоб яратиш ва нашрга тайёрлаш хизматлари учун "
        "махсус акциялар.\n\n"
        "📖 Китоб ёзиш\n"
        "🎨 Муқова дизайни\n"
        "📑 Саҳифалаш\n"
        "🔢 ISBN\n"
        "🌍 Amazon KDP\n\n"
        "📌 Амалдаги акциялар администратор томонидан янгиланади.",
        reply_markup=promotion_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "🎓 Илмий хизматлар акциялари")
async def scientific_promotions(message: Message):
    await message.answer(
        "🎓 <b>ИЛМИЙ ХИЗМАТЛАР АКЦИЯЛАРИ</b>\n\n"
        "Илмий хизматлар учун махсус чегирма ва таклифлар.\n\n"
        "📄 Илмий мақола\n"
        "📝 Тезис\n"
        "📚 Монография\n"
        "🌍 Халқаро мақола\n"
        "📊 Тақдимот\n\n"
        "📌 Амалдаги акциялар администратор томонидан янгиланади.",
        reply_markup=promotion_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "⬅️ Акциялар")
async def back_to_promotions(message: Message):
    await message.answer(
        "🔥 <b>АКЦИЯЛАР</b>\n\n"
        "Керакли бўлимни танланг 👇",
        reply_markup=promotions_menu(),
        parse_mode="HTML"
    )


@router.message(F.text == "🏠 Бош меню")
async def back_to_main(message: Message):
    await message.answer(
        "🏠 <b>Бош меню</b>\n\n"
        "Керакли бўлимни танланг 👇",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )