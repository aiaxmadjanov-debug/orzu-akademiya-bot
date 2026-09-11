from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from keyboards.design_menu import design_menu
from keyboards.main_menu import main_menu


router = Router()


def design_service_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📝 Буюртма бериш")
            ],
            [
                KeyboardButton(text="⬅️ Дизайн ва медиа")
            ],
            [
                KeyboardButton(text="🏠 Бош меню")
            ]
        ],
        resize_keyboard=True
    )


@router.message(F.text == "🎨 Дизайн ва медиа")
async def design_menu_handler(message: Message):
    await message.answer(
        "🎨 <b>ДИЗАЙН ВА МЕДИА</b>\n\n"
        "Бизнес, шахсий бренд, китоб ва ижтимоий тармоқлар учун "
        "профессионал дизайн ва медиа хизматлари.\n\n"
        "Керакли хизматни танланг 👇",
        reply_markup=design_menu(),
        parse_mode="HTML"
    )


@router.message(F.text == "🎨 Логотип")
async def logo_design(message: Message):
    await message.answer(
        "🎨 <b>ЛОГОТИП ДИЗАЙНИ</b>\n\n"
        "Брендингиз учун замонавий ва эсда қоларли логотип ишлаб чиқамиз.\n\n"
        "☑️ Концепция ишлаб чиқиш\n"
        "☑️ Логотип композицияси\n"
        "☑️ Ранг ва шрифт танлаш\n"
        "☑️ Бир нечта вариант\n"
        "☑️ PNG / JPG форматлар\n"
        "☑️ Вектор формат\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=design_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "📜 Сертификат / диплом")
async def certificate_design(message: Message):
    await message.answer(
        "📜 <b>СЕРТИФИКАТ / ДИПЛОМ ДИЗАЙНИ</b>\n\n"
        "Тадбир, курс, танлов ва ташкилотлар учун "
        "профессионал сертификат ва диплом дизайни.\n\n"
        "☑️ Замонавий дизайн\n"
        "☑️ Логотип жойлаштириш\n"
        "☑️ Исм ва маълумотларни жойлаштириш\n"
        "☑️ Print-ready формат\n"
        "☑️ Электрон вариант\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=design_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "📢 Реклама пост")
async def advertising_post(message: Message):
    await message.answer(
        "📢 <b>РЕКЛАМА ПОСТИ</b>\n\n"
        "Instagram, Telegram ва бошқа платформалар учун "
        "эътиборни тортадиган реклама дизайни.\n\n"
        "☑️ Пост дизайни\n"
        "☑️ Реклама баннери\n"
        "☑️ Матн композицияси\n"
        "☑️ Бренд услубига мослаш\n"
        "☑️ Instagram форматлари\n"
        "☑️ Telegram форматлари\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=design_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "🎬 Reels")
async def reels_video(message: Message):
    await message.answer(
        "🎬 <b>REELS ВИДЕО</b>\n\n"
        "Instagram ва TikTok учун қисқа, динамик ва "
        "рекламага мос видео роликлар тайёрлаймиз.\n\n"
        "☑️ Сценарий\n"
        "☑️ Монтаж\n"
        "☑️ Титрлар\n"
        "☑️ Музыка\n"
        "☑️ Transition ва эффектлар\n"
        "☑️ 9:16 вертикал формат\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=design_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "🤖 AI видео")
async def ai_video(message: Message):
    await message.answer(
        "🤖 <b>AI ВИДЕО</b>\n\n"
        "AI технологиялари ёрдамида реклама, ижтимоий тармоқ "
        "ва лойиҳалар учун креатив видеолар тайёрлаймиз.\n\n"
        "☑️ AI сценарий\n"
        "☑️ AI визуаллар\n"
        "☑️ AI анимация\n"
        "☑️ Овоз ва мусиқа\n"
        "☑️ Реклама формати\n"
        "☑️ 9:16 / 16:9 форматлар\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=design_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "🎤 Диктор овози")
async def voice_over(message: Message):
    await message.answer(
        "🎤 <b>ДИКТОР ОВОЗИ</b>\n\n"
        "Реклама, видео ва презентациялар учун профессионал "
        "диктор овози тайёрлаш хизмати.\n\n"
        "☑️ Ўзбек тили\n"
        "☑️ Рус тили\n"
        "☑️ Инглиз тили\n"
        "☑️ Реклама услуби\n"
        "☑️ Видео билан синхронлаш\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=design_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "📚 Китоб рекламаси")
async def book_advertising(message: Message):
    await message.answer(
        "📚 <b>КИТОБ РЕКЛАМАСИ</b>\n\n"
        "Китобингизни ижтимоий тармоқларда тарғиб қилиш учун "
        "креатив реклама материаллари тайёрлаймиз.\n\n"
        "☑️ Китоб рекламаси\n"
        "☑️ Пост дизайни\n"
        "☑️ Reels сценарийси\n"
        "☑️ Реклама видеоси\n"
        "☑️ Story формати\n"
        "☑️ Аудиторияга мос креатив\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=design_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "⬅️ Дизайн ва медиа")
async def back_to_design(message: Message):
    await message.answer(
        "🎨 <b>ДИЗАЙН ВА МЕДИА</b>\n\n"
        "Керакли хизматни танланг 👇",
        reply_markup=design_menu(),
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