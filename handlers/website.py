from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from keyboards.website_menu import website_menu
from keyboards.main_menu import main_menu


router = Router()


def website_service_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📝 Буюртма бериш")
            ],
            [
                KeyboardButton(text="⬅️ Сайт яратиш")
            ],
            [
                KeyboardButton(text="🏠 Бош меню")
            ]
        ],
        resize_keyboard=True
    )


@router.message(F.text == "🌐 Сайт яратиш")
async def website_menu_handler(message: Message):
    await message.answer(
        "🌐 <b>САЙТ ЯРАТИШ</b>\n\n"
        "Бизнес, шахсий бренд, муаллифлар ва хизматлар учун "
        "замонавий, профессионал ва телефонга мос веб-сайтлар яратамиз.\n\n"
        "☑️ Шахсий сайт\n"
        "☑️ Компания сайти\n"
        "☑️ Муаллиф сайти\n"
        "☑️ Хизматлар сайти\n"
        "☑️ Мобил қурилмаларга мос дизайн\n"
        "☑️ Telegram ва Instagram билан интеграция\n\n"
        "Керакли хизматни танланг 👇",
        reply_markup=website_menu(),
        parse_mode="HTML"
    )


@router.message(F.text == "🌐 Шахсий сайт")
async def personal_website(message: Message):
    await message.answer(
        "🌐 <b>ШАХСИЙ САЙТ</b>\n\n"
        "Сизнинг шахсий брендингиз, фаолиятингиз ва хизматларингизни "
        "тақдим этувчи замонавий веб-сайт.\n\n"
        "☑️ Шахсий маълумотлар\n"
        "☑️ Портфолио\n"
        "☑️ Хизматлар\n"
        "☑️ Контакт маълумотлари\n"
        "☑️ Адаптив дизайн\n"
        "☑️ Замонавий интерфейс\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=website_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "🏢 Компания сайти")
async def company_website(message: Message):
    await message.answer(
        "🏢 <b>КОМПАНИЯ САЙТИ</b>\n\n"
        "Компаниянгиз, маҳсулотларингиз ва хизматларингизни "
        "профессионал тақдим этувчи корпоратив веб-сайт.\n\n"
        "☑️ Компания ҳақида\n"
        "☑️ Хизматлар\n"
        "☑️ Лойиҳалар\n"
        "☑️ Жамоа\n"
        "☑️ Контактлар\n"
        "☑️ Мобил версия\n"
        "☑️ Админ бошқаруви\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=website_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "📚 Муаллиф сайти")
async def author_website(message: Message):
    await message.answer(
        "📚 <b>МУАЛЛИФ САЙТИ</b>\n\n"
        "Ёзувчи, олим ёки ижодкорлар учун шахсий муаллифлик веб-сайти.\n\n"
        "☑️ Муаллиф ҳақида\n"
        "☑️ Китоблар\n"
        "☑️ Илмий ишлар\n"
        "☑️ Янгиликлар\n"
        "☑️ Портфолио\n"
        "☑️ Алоқа формаси\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=website_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "🛍 Хизматлар сайти")
async def services_website(message: Message):
    await message.answer(
        "🛍 <b>ХИЗМАТЛАР САЙТИ</b>\n\n"
        "Хизматларингизни онлайн тақдим этиш ва мижозлардан "
        "буюртма қабул қилиш учун веб-сайт.\n\n"
        "☑️ Хизматлар каталоги\n"
        "☑️ Хизмат тавсифи\n"
        "☑️ Нарҳлар бўлими\n"
        "☑️ Буюртма формаси\n"
        "☑️ Мижозлар фикри\n"
        "☑️ Telegram билан боғлаш\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=website_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "📱 Телефонга мос дизайн")
async def responsive_design(message: Message):
    await message.answer(
        "📱 <b>ТЕЛЕФОНГА МОС ДИЗАЙН</b>\n\n"
        "Сайт барча экранларда — телефон, планшет ва компьютерда "
        "қулай кўриниши учун адаптив дизайн асосида тайёрланади.\n\n"
        "☑️ Mobile-first ёндашув\n"
        "☑️ Планшет версияси\n"
        "☑️ Desktop версияси\n"
        "☑️ Қулай навигация\n"
        "☑️ Турли экранларга мослашув\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=website_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "💬 Telegram ва Instagram")
async def social_integration(message: Message):
    await message.answer(
        "💬 <b>TELEGRAM ВА INSTAGRAM БИЛАН БОҒЛАШ</b>\n\n"
        "Сайтингизни Telegram ва Instagram платформалари билан "
        "боғлаш ва мижозлар учун қулай алоқа каналларини ташкил қилиш.\n\n"
        "☑️ Telegram тугмаси\n"
        "☑️ Instagram ҳаволаси\n"
        "☑️ Мурожаат формаси\n"
        "☑️ Ижтимоий тармоқларга йўналтириш\n"
        "☑️ Мижоз билан тезкор алоқа\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=website_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "⬅️ Сайт яратиш")
async def back_to_website(message: Message):
    await message.answer(
        "🌐 <b>САЙТ ЯРАТИШ</b>\n\n"
        "Керакли хизматни танланг 👇",
        reply_markup=website_menu(),
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