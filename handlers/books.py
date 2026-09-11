from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from keyboards.book_menu import book_menu
from keyboards.main_menu import main_menu


router = Router()


# =========================================================
# 📚 KITOB VA NASHRIYOT
# =========================================================

@router.message(F.text == "📚 Китоб ва нашриёт")
async def books_menu_handler(
    message: Message,
    state: FSMContext
):
    await state.clear()

    await message.answer(
        "📚 <b>КИТОБ ВА НАШРИЁТ</b>\n\n"
        "Китоб чиқариш ниятингиз борми?\n\n"
        "<b>ORZU AKADEMIYA</b> ғоядан бошлаб тайёр китобгача "
        "бўлган жараёнда сиз билан бирга! 📖\n\n"
        "Керакли хизматни танланг 👇",
        reply_markup=book_menu(),
        parse_mode="HTML"
    )


# =========================================================
# 🧩 XIZMAT MENYUSI
# =========================================================

def book_service_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📝 Буюртма бериш")
            ],
            [
                KeyboardButton(text="⬅️ Китоб ва нашриёт")
            ],
            [
                KeyboardButton(text="🏠 Бош меню")
            ]
        ],
        resize_keyboard=True
    )


# =========================================================
# 📖 KITOB YOZISH
# =========================================================

@router.message(F.text == "📖 Китоб ёзиш")
async def book_writing(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        service="📖 Китоб ёзиш"
    )

    await message.answer(
        "📖 <b>КИТОБ ЁЗИШ</b>\n\n"
        "Ғоянгиз бор, лекин уни китобга айлантиришни билмаяпсизми?\n\n"
        "Биз сизга ғоядан тайёр китоб концепциясигача ёрдам берамиз:\n\n"
        "☑️ Китоб концепциясини ишлаб чиқиш\n"
        "☑️ Мундарижа тузиш\n"
        "☑️ Бобларни профессионал ёзиш\n"
        "☑️ Матнни таҳрир қилиш\n"
        "☑️ Амалий машқлар қўшиш\n"
        "☑️ Муаллиф услубини сақлаш\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=book_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# ✍️ MATN TAHRIRI
# =========================================================

@router.message(F.text == "✍️ Матн таҳрири")
async def text_editing(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        service="✍️ Матн таҳрири"
    )

    await message.answer(
        "✍️ <b>МАТН ТАҲРИРИ</b>\n\n"
        "Матнингизни мазмун, услуб ва тил жиҳатидан профессионал таҳрирлаймиз.\n\n"
        "☑️ Матн мазмунини таҳлил қилиш\n"
        "☑️ Услубий таҳрир\n"
        "☑️ Имло ва грамматика\n"
        "☑️ Матн мантиқийлигини яхшилаш\n"
        "☑️ Нашрга тайёрлаш\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=book_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 📝 KORREKTURA
# =========================================================

@router.message(F.text == "📝 Корректура")
async def proofreading(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        service="📝 Корректура"
    )

    await message.answer(
        "📝 <b>КОРРЕКТУРА</b>\n\n"
        "Тайёр матндаги имло, пунктуация ва техник хатоларни текширамиз.\n\n"
        "☑️ Имло хатолари\n"
        "☑️ Тиниш белгилари\n"
        "☑️ Сўз ва жумла хатолари\n"
        "☑️ Техник хатолар\n"
        "☑️ Нашрга тайёр ҳолатга келтириш\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=book_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 🎨 MUQOVA DIZAYNI
# =========================================================

@router.message(F.text == "🎨 Муқова дизайни")
async def cover_design(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        service="🎨 Муқова дизайни"
    )

    await message.answer(
        "🎨 <b>КИТОБ МУҚОВАСИ ДИЗАЙНИ</b>\n\n"
        "Китобингиз учун профессионал ва нашрга тайёр муқова дизайни.\n\n"
        "☑️ Олд муқова\n"
        "☑️ Орқа муқова\n"
        "☑️ Корешок\n"
        "☑️ Профессионал композиция\n"
        "☑️ Нашрга тайёр формат\n"
        "☑️ Amazon KDP формати\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=book_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 📑 SAHIFALASH
# =========================================================

@router.message(F.text == "📑 Саҳифалаш")
async def book_layout(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        service="📑 Саҳифалаш"
    )

    await message.answer(
        "📑 <b>КИТОБ САҲИФАЛАШ</b>\n\n"
        "Китоб матнини профессионал тарзда саҳифалаймиз ва нашрга тайёрлаймиз.\n\n"
        "☑️ Саҳифа композицияси\n"
        "☑️ Шрифт ва интерваллар\n"
        "☑️ Боблар дизайни\n"
        "☑️ Расм ва жадвалларни жойлаш\n"
        "☑️ Print-ready файл\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=book_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 🔎 PLAGIAT
# =========================================================

@router.message(F.text == "🔎 Плагиат текшируви")
async def plagiarism_check(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        service="🔎 Плагиат текшируви"
    )

    await message.answer(
        "🔎 <b>ПЛАГИАТ ТЕКШИРУВИ</b>\n\n"
        "Матнингизнинг ўхшашлик даражасини текшириш ва натижани таҳлил қилиш хизмати.\n\n"
        "☑️ Матнни текшириш\n"
        "☑️ Ўхшашлик натижасини таҳлил қилиш\n"
        "☑️ Манбаларни аниқлаш\n"
        "☑️ Ҳисобот тайёрлаш\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=book_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 🔢 ISBN
# =========================================================

@router.message(F.text == "🔢 ISBN")
async def isbn_service(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        service="🔢 ISBN"
    )

    await message.answer(
        "🔢 <b>ISBN РАСМИЙЛАШТИРИШ</b>\n\n"
        "Китобингизни нашрга тайёрлаш жараёнида ISBN бўйича хизмат кўрсатамиз.\n\n"
        "☑️ ISBN жараёни бўйича маслаҳат\n"
        "☑️ Керакли маълумотларни тайёрлаш\n"
        "☑️ Нашр жараёнига мослаш\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=book_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 📚 MONOGRAFIYA
# =========================================================

@router.message(F.text == "📚 Монография")
async def monograph(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        service="📚 Монография"
    )

    await message.answer(
        "📚 <b>МОНОГРАФИЯ ТАЙЁРЛАШ</b>\n\n"
        "Илмий мавзудаги монографияни шакллантириш, таҳрирлаш ва нашрга тайёрлашда ёрдам берамиз.\n\n"
        "☑️ Тузилма ишлаб чиқиш\n"
        "☑️ Матнни шакллантириш\n"
        "☑️ Илмий таҳрир\n"
        "☑️ Манбаларни тартиблаш\n"
        "☑️ Саҳифалаш ва нашрга тайёрлаш\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=book_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 🌍 AMAZON KDP
# =========================================================

@router.message(F.text == "🌍 Amazon KDP")
async def amazon_kdp(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        service="🌍 Amazon KDP"
    )

    await message.answer(
        "🌍 <b>AMAZON KDP УЧУН КИТОБ ТАЙЁРЛАШ</b>\n\n"
        "Китобингизни Amazon KDP талабларига мослаштиришда ёрдам берамиз.\n\n"
        "☑️ Interior файл\n"
        "☑️ Cover файл\n"
        "☑️ KDP формат талаблари\n"
        "☑️ Print-ready тайёрлаш\n"
        "☑️ Электрон ва босма форматлар\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=book_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 🇬🇧 TARJIMA
# =========================================================

@router.message(F.text == "🇬🇧 Таржима")
async def translation(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        service="🇬🇧 Таржима"
    )

    await message.answer(
        "🇬🇧 <b>КИТОБНИ ИНГЛИЗ ТИЛИГА ТАРЖИМА ҚИЛИШ</b>\n\n"
        "Китоб матнини мазмун ва услубни сақлаган ҳолда инглиз тилига таржима қилиш хизмати.\n\n"
        "☑️ Профессионал таржима\n"
        "☑️ Терминологияни сақлаш\n"
        "☑️ Муаллиф услубини сақлаш\n"
        "☑️ Таҳрир ва корректура\n\n"
        "📝 Буюртма бериш учун қуйидаги тугмани босинг.",
        reply_markup=book_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# ⬅️ KITOB MENYUSIGA QAYTISH
# =========================================================

@router.message(F.text == "⬅️ Китоб ва нашриёт")
async def back_to_books(
    message: Message,
    state: FSMContext
):
    await state.clear()

    await message.answer(
        "📚 <b>КИТОБ ВА НАШРИЁТ</b>\n\n"
        "Керакли хизматни танланг 👇",
        reply_markup=book_menu(),
        parse_mode="HTML"
    )


# =========================================================
# 🏠 BOSH MENYU
# =========================================================

@router.message(F.text == "🏠 Бош меню")
async def back_to_main_menu(
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