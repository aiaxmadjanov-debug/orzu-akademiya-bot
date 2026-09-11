from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from keyboards.scientific_menu import scientific_menu
from keyboards.main_menu import main_menu


router = Router()


def scientific_service_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📝 Буюртма бериш")
            ],
            [
                KeyboardButton(text="⬅️ Илмий хизматлар")
            ],
            [
                KeyboardButton(text="🏠 Бош меню")
            ]
        ],
        resize_keyboard=True
    )


# =========================================================
# 🎓 ILMIY XIZMATLAR
# =========================================================

@router.message(F.text == "🎓 Илмий хизматлар")
async def scientific_menu_handler(
    message: Message,
    state: FSMContext
):
    await state.clear()

    await message.answer(
        "🎓 <b>ИЛМИЙ ХИЗМАТЛАР</b>\n\n"
        "Илмий ишларингизни профессионал тайёрлаш, таҳрирлаш "
        "ва талабларга мослаштиришда ёрдам берамиз.\n\n"
        "Керакли хизматни танланг 👇",
        reply_markup=scientific_menu(),
        parse_mode="HTML"
    )


# =========================================================
# 📄 ILMIY MAQOLA
# =========================================================

@router.message(F.text == "📄 Илмий мақола")
async def scientific_article(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        service="📄 Илмий мақола"
    )

    await message.answer(
        "📄 <b>ИЛМИЙ МАҚОЛА</b>\n\n"
        "Мавзунгизга мос илмий мақолани шакллантириш, "
        "таҳрир қилиш ва белгиланган талабларга мослаштириш хизмати.\n\n"
        "☑️ IMRAD структураси\n"
        "☑️ Аннотация\n"
        "☑️ Калит сўзлар\n"
        "☑️ Кириш\n"
        "☑️ Методология\n"
        "☑️ Натижалар ва таҳлил\n"
        "☑️ Хулоса\n"
        "☑️ Фойдаланилган адабиётлар\n\n"
        "📌 Мавзу, йўналиш ва топшириш муддатини юборинг.\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=scientific_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 📝 TEZIS
# =========================================================

@router.message(F.text == "📝 Тезис")
async def thesis(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        service="📝 Тезис"
    )

    await message.answer(
        "📝 <b>ТЕЗИС ТАЙЁРЛАШ</b>\n\n"
        "Конференция ва илмий тадбирлар учун тезисни талабларга "
        "мос тарзда тайёрлашда ёрдам берамиз.\n\n"
        "☑️ Мавзуни шакллантириш\n"
        "☑️ Асосий ғояларни ажратиш\n"
        "☑️ Илмий услуб\n"
        "☑️ Талаб қилинган ҳажмга мослаш\n"
        "☑️ Манбаларни тартиблаш\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=scientific_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 📚 MONOGRAFIYA
# =========================================================

@router.message(F.text == "📚 Монография")
async def scientific_monograph(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        service="📚 Монография"
    )

    await message.answer(
        "📚 <b>МОНОГРАФИЯ</b>\n\n"
        "Илмий мавзудаги монографияни шакллантириш, "
        "таҳрирлаш ва нашрга тайёрлашда ёрдам берамиз.\n\n"
        "☑️ Тузилма ишлаб чиқиш\n"
        "☑️ Илмий матнни шакллантириш\n"
        "☑️ Илмий таҳрир\n"
        "☑️ Манбалар билан ишлаш\n"
        "☑️ Хулоса ва тавсиялар\n"
        "☑️ Нашрга тайёрлаш\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=scientific_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 🎓 MAGISTRLIK ISHI
# =========================================================

@router.message(F.text == "🎓 Магистрлик иши")
async def masters_thesis(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        service="🎓 Магистрлик иши"
    )

    await message.answer(
        "🎓 <b>МАГИСТРЛИК ИШИ БЎЙИЧА ТАҲРИР ВА МАСЛАҲАТ</b>\n\n"
        "Магистрлик ишингизни илмий талаблар асосида "
        "кўриб чиқиш ва такомиллаштиришда ёрдам берамиз.\n\n"
        "☑️ Тузилмани таҳлил қилиш\n"
        "☑️ Илмий услубни яхшилаш\n"
        "☑️ Манбаларни тартиблаш\n"
        "☑️ Матнни таҳрир қилиш\n"
        "☑️ Техник талабларга мослаштириш\n\n"
        "📌 Хизмат маслаҳат ва таҳрирга қаратилган.\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=scientific_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 🌍 XALQARO MAQOLA
# =========================================================

@router.message(F.text == "🌍 Халқаро мақола")
async def international_article(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        service="🌍 Халқаро мақола"
    )

    await message.answer(
        "🌍 <b>ХАЛҚАРО ЖУРНАЛ УЧУН МАҚОЛА</b>\n\n"
        "Халқаро журнал талабларига мос илмий мақолани "
        "тайёрлаш ва таҳрирлаш хизмати.\n\n"
        "☑️ Журнал талабларини таҳлил қилиш\n"
        "☑️ Илмий структура\n"
        "☑️ Abstract\n"
        "☑️ Keywords\n"
        "☑️ Academic English таҳрири\n"
        "☑️ Манбаларни тартиблаш\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=scientific_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 📊 TAQDIMOT
# =========================================================

@router.message(F.text == "📊 Тақдимот")
async def scientific_presentation(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        service="📊 Тақдимот"
    )

    await message.answer(
        "📊 <b>ИЛМИЙ ТАҚДИМОТ</b>\n\n"
        "Ҳимоя, конференция ва илмий тадбирлар учун "
        "профессионал тақдимот тайёрлаймиз.\n\n"
        "☑️ Слайдлар структураси\n"
        "☑️ Матнни қисқартириш ва тизимлаш\n"
        "☑️ Диаграмма ва жадваллар\n"
        "☑️ Профессионал дизайн\n"
        "☑️ PPTX формати\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=scientific_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 🔎 PLAGIAT
# =========================================================

@router.message(F.text == "🔎 Плагиат текшируви")
async def scientific_plagiarism(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        service="🔎 Плагиат текшируви"
    )

    await message.answer(
        "🔎 <b>ПЛАГИАТ ТЕКШИРУВИ</b>\n\n"
        "Илмий ишингиздаги ўхшашлик даражасини текшириш "
        "ва натижани таҳлил қилиш хизмати.\n\n"
        "☑️ Матнни текшириш\n"
        "☑️ Ўхшашликни таҳлил қилиш\n"
        "☑️ Манбаларни кўриб чиқиш\n"
        "☑️ Ҳисоботни таҳлил қилиш\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=scientific_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 📑 MANBALAR
# =========================================================

@router.message(F.text == "📑 Манбалар ва адабиётлар")
async def sources_formatting(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        service="📑 Манбалар ва адабиётлар"
    )

    await message.answer(
        "📑 <b>МАНБАЛАР ВА АДАБИЁТЛАРНИ ТАРТИБЛАШ</b>\n\n"
        "Фойдаланилган манбалар рўйхатини белгиланган "
        "стандарт ва талабларга мослаштирамиз.\n\n"
        "☑️ Адабиётлар рўйхатини тузиш\n"
        "☑️ Манбаларни бир хил форматга келтириш\n"
        "☑️ Матн ичидаги ҳаволаларни текшириш\n"
        "☑️ Библиографик тартиб\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=scientific_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# ⬅️ ORTGA
# =========================================================

@router.message(F.text == "⬅️ Илмий хизматлар")
async def back_to_scientific(
    message: Message,
    state: FSMContext
):
    await state.clear()

    await message.answer(
        "🎓 <b>ИЛМИЙ ХИЗМАТЛАР</b>\n\n"
        "Керакли хизматни танланг 👇",
        reply_markup=scientific_menu(),
        parse_mode="HTML"
    )


# =========================================================
# 🏠 BOSH MENU
# =========================================================

@router.message(F.text == "🏠 Бош меню")
async def back_to_main(
    message: Message,
    state: FSMContext
):
    await state.clear()

    await message.answer(
        "🏠 <b>Бош меню</b>\n\n"
        "Керакли бўлимни танланг 👇",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )