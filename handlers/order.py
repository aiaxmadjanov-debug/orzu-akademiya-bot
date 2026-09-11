from datetime import datetime
import uuid

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from states.order_states import OrderStates
from keyboards.order_menu import order_cancel_menu, order_confirm_menu
from keyboards.main_menu import main_menu

from keyboards.book_menu import book_menu
from keyboards.scientific_menu import scientific_menu
from keyboards.contest_menu import contest_menu
from keyboards.design_menu import design_menu
from keyboards.website_menu import website_menu

from config import ADMIN_ID
from database.db import async_session, Order


router = Router()


# =========================================================
# 📚 BUYURTMA ICHIDAGI XIZMATLAR MENYUSI
# =========================================================

def service_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📚 Китоб ва нашриёт"),
                KeyboardButton(text="🎓 Илмий хизматлар")
            ],
            [
                KeyboardButton(text="🏆 Танлов ва лойиҳалар"),
                KeyboardButton(text="🎨 Дизайн ва медиа")
            ],
            [
                KeyboardButton(text="🌐 Сайт яратиш")
            ],
            [
                KeyboardButton(text="❌ Буюртмани бекор қилиш")
            ]
        ],
        resize_keyboard=True
    )


# =========================================================
# 🏠 ASOSIY BO‘LIMLARNI OCHISH
#
# Muhim:
# waiting_service bosqichida bu handlerlar ishlamaydi.
# Chunki u yerda foydalanuvchi xizmat yo‘nalishini tanlaydi.
#
# Keyingi bosqichlarda esa foydalanuvchi asosiy bo‘limga
# qaytsa, FSM tozalanadi va bo‘lim ochiladi.
# =========================================================

MAIN_SECTION_TEXTS = {
    "📚 Китоб ва нашриёт",
    "🎓 Илмий хизматлар",
    "🏆 Танлов ва лойиҳалар",
    "🎨 Дизайн ва медиа",
    "🌐 Сайт яратиш"
}


@router.message(
    OrderStates.waiting_name,
    F.text.in_(MAIN_SECTION_TEXTS)
)
@router.message(
    OrderStates.waiting_phone,
    F.text.in_(MAIN_SECTION_TEXTS)
)
@router.message(
    OrderStates.waiting_task,
    F.text.in_(MAIN_SECTION_TEXTS)
)
@router.message(
    OrderStates.waiting_volume,
    F.text.in_(MAIN_SECTION_TEXTS)
)
@router.message(
    OrderStates.waiting_deadline,
    F.text.in_(MAIN_SECTION_TEXTS)
)
@router.message(
    OrderStates.waiting_file,
    F.text.in_(MAIN_SECTION_TEXTS)
)
@router.message(
    OrderStates.confirming,
    F.text.in_(MAIN_SECTION_TEXTS)
)
async def open_main_section_from_order(
    message: Message,
    state: FSMContext
):
    section = message.text

    # Eski buyurtma jarayonini tozalaymiz
    await state.clear()

    # =====================================================
    # 📚 KITOB
    # =====================================================

    if section == "📚 Китоб ва нашриёт":
        await message.answer(
            "📚 <b>КИТОБ ВА НАШРИЁТ</b>\n\n"
            "Китоб чиқариш ниятингиз борми?\n\n"
            "<b>ORZU AKADEMIYA</b> ғоядан бошлаб тайёр "
            "китобгача бўлган жараёнда сиз билан бирга! 📖\n\n"
            "Керакли хизматни танланг 👇",
            reply_markup=book_menu(),
            parse_mode="HTML"
        )
        return

    # =====================================================
    # 🎓 ILMIY
    # =====================================================

    if section == "🎓 Илмий хизматлар":
        await message.answer(
            "🎓 <b>ИЛМИЙ ХИЗМАТЛАР</b>\n\n"
            "Илмий ишларингизни профессионал тайёрлаш, "
            "таҳрирлаш ва талабларга мослаштиришда ёрдам берамиз.\n\n"
            "Керакли хизматни танланг 👇",
            reply_markup=scientific_menu(),
            parse_mode="HTML"
        )
        return

    # =====================================================
    # 🏆 TANLOV
    # =====================================================

    if section == "🏆 Танлов ва лойиҳалар":
        await message.answer(
            "🏆 <b>ТАНЛОВ ВА ЛОЙИҲАЛАР</b>\n\n"
            "ORZU AKADEMIYA томонидан илмий, ижодий ва "
            "ижтимоий йўналишдаги лойиҳалар ва танловлар.\n\n"
            "🔥 Жорий танловлар\n"
            "🏅 Миллат Ғурури\n"
            "🏆 Шифо Элчиси\n"
            "🧠 Онг ва Шифо\n"
            "🌷 Азизим Онам\n"
            "📚 Илмий мақола танловлари\n\n"
            "Керакли бўлимни танланг 👇",
            reply_markup=contest_menu(),
            parse_mode="HTML"
        )
        return

    # =====================================================
    # 🎨 DESIGN
    # =====================================================

    if section == "🎨 Дизайн ва медиа":
        await message.answer(
            "🎨 <b>ДИЗАЙН ВА МЕДИА</b>\n\n"
            "Бизнес, шахсий бренд, китоб ва ижтимоий "
            "тармоқлар учун профессионал дизайн ва медиа хизматлари.\n\n"
            "Керакли хизматни танланг 👇",
            reply_markup=design_menu(),
            parse_mode="HTML"
        )
        return

    # =====================================================
    # 🌐 WEBSITE
    # =====================================================

    if section == "🌐 Сайт яратиш":
        await message.answer(
            "🌐 <b>САЙТ ЯРАТИШ</b>\n\n"
            "Бизнес, шахсий бренд, муаллифлар ва хизматлар "
            "учун замонавий, профессионал ва телефонга мос "
            "веб-сайтлар яратамиз.\n\n"
            "☑️ Шахсий сайт\n"
            "☑️ Компания сайти\n"
            "☑️ Муаллиф сайти\n"
            "☑️ Хизматлар сайти\n"
            "☑️ Мобил қурилмаларга мос дизайн\n"
            "☑️ Telegram ва Instagram интеграцияси\n\n"
            "Керакли хизматни танланг 👇",
            reply_markup=website_menu(),
            parse_mode="HTML"
        )
        return


# =========================================================
# 📝 BUYURTMA BOSHLASH
# =========================================================

@router.message(F.text == "📝 Буюртма бериш")
async def start_order(
    message: Message,
    state: FSMContext
):
    # Oldindan tanlangan xizmatni olamiz
    old_data = await state.get_data()
    selected_service = old_data.get("service")

    # FSMni tozalaymiz, lekin tanlangan xizmatni saqlab qolamiz
    await state.clear()

    if not selected_service:
        await message.answer(
            "⚠️ Аввало хизматни танланг.\n\n"
            "Керакли хизматни танлаб, кейин "
            "📝 <b>Буюртма бериш</b> тугмасини босинг.",
            reply_markup=main_menu(),
            parse_mode="HTML"
        )
        return

    await state.update_data(
        service=selected_service,
        name=message.from_user.full_name,
        phone="—"
    )

    # =====================================================
    # 📑 САҲИФАЛАШ
    # =====================================================

    if selected_service == "📑 Саҳифалаш":

        await state.set_state(
            OrderStates.waiting_layout_pages
        )

        await message.answer(
            "📑 <b>САҲИФАЛАШ БУЮРТМАСИ</b>\n\n"
            "Сиз <b>«Саҳифалаш»</b> хизматини танладингиз.\n\n"
            "Энди шу хизмат учун керакли маълумотларни "
            "босқичма-босқич киритамиз.\n\n"
            "1️⃣ 📄 <b>Китоб неча бетдан иборат?</b>\n\n"
            "Масалан:\n"
            "• <i>120 бет</i>\n"
            "• <i>250 бет</i>\n"
            "• <i>350 бет</i>",
            reply_markup=order_cancel_menu(),
            parse_mode="HTML"
        )

        return

    # =====================================================
    # 🔎 БОШҚА ХИЗМАТЛАР
    # =====================================================

    await state.set_state(
        OrderStates.waiting_task
    )

    await message.answer(
        "📝 <b>БУЮРТМА МАЪЛУМОТЛАРИ</b>\n\n"
        f"📚 <b>Хизмат:</b> {selected_service}\n\n"
        "📝 <b>Мавзу ёки вазифани ёзинг:</b>\n\n"
        "Нима тайёрлаш кераклигини имкони борича "
        "аниқ ёзинг.\n\n"
        "Масалан:\n"
        "• <i>150 бетлик китобни таҳрирлаш керак</i>\n"
        "• <i>Китоб муқовасини тайёрлаш керак</i>\n"
        "• <i>Матнни плагиатга текшириш керак</i>",
        reply_markup=order_cancel_menu(),
        parse_mode="HTML"
    )
    # =====================================================
    # 📑 САҲИФАЛАШ
    # =====================================================

    if selected_service == "📑 Саҳифалаш":

        await state.set_state(
            OrderStates.waiting_layout_pages
        )

        await message.answer(
            "📑 <b>САҲИФАЛАШ БУЮРТМАСИ</b>\n\n"
            "Сиз <b>«Саҳифалаш»</b> хизматини танладингиз.\n\n"
            "Энди шу хизмат учун керакли маълумотларни "
            "босқичма-босқич киритамиз.\n\n"
            "1️⃣ 📄 <b>Китоб неча бетдан иборат?</b>\n\n"
            "Масалан:\n"
            "• <i>120 бет</i>\n"
            "• <i>250 бет</i>\n"
            "• <i>350 бет</i>",
            reply_markup=order_cancel_menu(),
            parse_mode="HTML"
        )

        return

    # =====================================================
    # 🔎 БОШҚА ХИЗМАТЛАР
    # =====================================================

    await state.set_state(
        OrderStates.waiting_task
    )

    await message.answer(
        "📝 <b>БУЮРТМА МАЪЛУМОТЛАРИ</b>\n\n"
        f"📚 <b>Хизмат:</b> {selected_service}\n\n"
        "📝 <b>Мавзу ёки вазифани ёзинг:</b>\n\n"
        "Нима тайёрлаш кераклигини имкони борича "
        "аниқ ёзинг.\n\n"
        "Масалан:\n"
        "• <i>150 бетлик китобни таҳрирлаш керак</i>\n"
        "• <i>Китоб муқовасини тайёрлаш керак</i>\n"
        "• <i>Матнни плагиатга текшириш керак</i>",
        reply_markup=order_cancel_menu(),
        parse_mode="HTML"
    )
# =========================================================
# 📑 SAHIFALASH — BET SONI
# =========================================================

@router.message(OrderStates.waiting_layout_pages)
async def get_layout_page_count(
    message: Message,
    state: FSMContext
):
    page_count = message.text.strip()

    # Bo'sh javobni qabul qilmaymiz
    if not page_count:
        await message.answer(
            "⚠️ Илтимос, бетлар сонини киритинг.\n\n"
            "Масалан: <i>120 бет</i>",
            reply_markup=order_cancel_menu(),
            parse_mode="HTML"
        )
        return

    await state.update_data(
        page_count=page_count
    )

    # Keyingi savol
    await state.set_state(
    OrderStates.waiting_layout_format
)

    await message.answer(
        "📐 <b>2️⃣ КИТОБ ФОРМАТИ</b>\n\n"
        "Китоб қайси форматда саҳифаланиши керак?\n\n"
        "Масалан:\n"
        "• <i>A4</i>\n"
        "• <i>A5</i>\n"
        "• <i>B5</i>\n"
        "• <i>Бошқа формат</i>\n\n"
        "Агар аниқ форматни билмасангиз, "
        "<b>«Билмайман»</b> деб ёзинг.",
        reply_markup=order_cancel_menu(),
        parse_mode="HTML"
    )
# =========================================================
# 📐 SAHIFALASH — FORMAT
# =========================================================

@router.message(OrderStates.waiting_layout_format)
async def get_layout_format(
    message: Message,
    state: FSMContext
):
    layout_format = message.text.strip()

    if not layout_format:
        await message.answer(
            "⚠️ Илтимос, китоб форматини киритинг.\n\n"
            "Масалан: <i>A4</i>, <i>A5</i>, <i>B5</i> "
            "ёки <i>Билмайман</i>.",
            reply_markup=order_cancel_menu(),
            parse_mode="HTML"
        )
        return

    data = await state.get_data()
    selected_service = data.get("service")

    # Фақат Саҳифалаш учун форматни сақлаймиз
    if selected_service == "📑 Саҳифалаш":
        await state.update_data(
            layout_format=layout_format
        )

        await state.set_state(
    OrderStates.waiting_layout_file_type
)

        await message.answer(
            "📄 <b>3️⃣ ФАЙЛ ФОРМАТИ</b>\n\n"
            "Сиздаги китоб матни қайси файл кўринишида?\n\n"
            "Масалан:\n"
            "• <i>Word (.docx)</i>\n"
            "• <i>PDF</i>\n"
            "• <i>Excel</i>\n"
            "• <i>Бир нечта файл</i>\n"
            "• <i>Бошқа</i>\n\n"
            "Файл турини ёзинг.",
            reply_markup=order_cancel_menu(),
            parse_mode="HTML"
        )
        return

    # Бошқа хизматлар учун эски оқим
    await state.update_data(
        task=layout_format
    )

    await state.set_state(
        OrderStates.waiting_volume
    )

    await message.answer(
        "📑 <b>ҲАЖМ</b>\n\n"
        "Буюртма ҳажмини киритинг.\n\n"
        "Масалан: <i>150 бет</i>",
        reply_markup=order_cancel_menu(),
        parse_mode="HTML"
    )
# =========================================================
# 📄 SAHIFALASH — FAYL TURI
# =========================================================

@router.message(OrderStates.waiting_layout_file_type)
async def get_layout_file_type(
    message: Message,
    state: FSMContext
):
    file_type = message.text.strip()

    if not file_type:
        await message.answer(
            "⚠️ Илтимос, файл турини киритинг.\n\n"
            "Масалан: <i>Word (.docx)</i>, <i>PDF</i> "
            "ёки <i>Бир нечта файл</i>.",
            reply_markup=order_cancel_menu(),
            parse_mode="HTML"
        )
        return

    await state.update_data(
        layout_file_type=file_type
    )

    await state.set_state(
        OrderStates.waiting_layout_design
    )

    await message.answer(
        "🎨 <b>4️⃣ ДИЗАЙН ТАЛАБИ</b>\n\n"
        "Саҳифалашда махсус дизайн ёки услубий талабингиз борми?\n\n"
        "Масалан:\n"
        "• <i>Оддий ва минимал дизайн</i>\n"
        "• <i>Ҳар бир боб алоҳида дизайнда</i>\n"
        "• <i>Расм ва жадваллар билан</i>\n"
        "• <i>Мавжуд намуна асосида</i>\n"
        "• <i>Махсус талаб йўқ</i>\n\n"
        "Талабингизни ёзинг.",
        reply_markup=order_cancel_menu(),
        parse_mode="HTML"
    )
# =========================================================
# 🎨 SAHIFALASH — DIZAYN TALABI
# =========================================================

@router.message(OrderStates.waiting_layout_design)
async def get_layout_design(
    message: Message,
    state: FSMContext
):
    design_requirement = message.text.strip()

    if not design_requirement:
        await message.answer(
            "⚠️ Илтимос, дизайн талабини ёзинг.\n\n"
            "Агар махсус талаб бўлмаса:\n"
            "<i>Махсус талаб йўқ</i> деб ёзинг.",
            reply_markup=order_cancel_menu(),
            parse_mode="HTML"
        )
        return

    await state.update_data(
        layout_design=design_requirement
    )

    await state.set_state(
        OrderStates.waiting_layout_deadline
    )

    await message.answer(
        "⏰ <b>5️⃣ МУДДАТ</b>\n\n"
        "Тайёр саҳифаланган файл қачонга керак?\n\n"
        "Масалан:\n"
        "• <i>3 кун ичида</i>\n"
        "• <i>10 сентябргача</i>\n"
        "• <i>Имкон қадар тезроқ</i>\n"
        "• <i>Аниқ муддат йўқ</i>\n\n"
        "Муддатни ёзинг.",
        reply_markup=order_cancel_menu(),
        parse_mode="HTML"
    )
# =========================================================
# ⏰ SAHIFALASH — MUDDAT
# =========================================================

@router.message(OrderStates.waiting_layout_deadline)
async def get_layout_deadline(
    message: Message,
    state: FSMContext
):
    deadline = message.text.strip()

    if not deadline:
        await message.answer(
            "⚠️ Илтимос, муддатни киритинг.\n\n"
            "Масалан: <i>10 сентябргача</i>.",
            reply_markup=order_cancel_menu(),
            parse_mode="HTML"
        )
        return

    await state.update_data(
        layout_deadline=deadline,
        deadline=deadline
    )

    await state.set_state(
        OrderStates.waiting_layout_file
    )

    await message.answer(
        "📎 <b>6️⃣ ФАЙЛНИ ЮБОРИНГ</b>\n\n"
        "Саҳифалаш керак бўлган китоб матнини "
        "шу ерга юборинг.\n\n"
        "📄 Word, PDF ёки бошқа файл юборишингиз мумкин.\n\n"
        "Агар ҳозирча файл тайёр бўлмаса, "
        "<b>«Файл йўқ»</b> деб ёзинг.",
        reply_markup=order_cancel_menu(),
        parse_mode="HTML"
    )
# =========================================================
# 📎 SAHIFALASH — FAYL QABUL QILISH
# =========================================================

@router.message(
    OrderStates.waiting_layout_file,
    F.document
)
async def get_layout_document(
    message: Message,
    state: FSMContext
):
    document = message.document

    await state.update_data(
        file_id=document.file_id,
        file_type="document",
        file_name=document.file_name or "Файл"
    )

    await show_layout_confirmation(
        message,
        state
    )


# =========================================================
# 🖼 SAHIFALASH — RASM/FAYL
# =========================================================

@router.message(
    OrderStates.waiting_layout_file,
    F.photo
)
async def get_layout_photo(
    message: Message,
    state: FSMContext
):
    photo = message.photo[-1]

    await state.update_data(
        file_id=photo.file_id,
        file_type="photo",
        file_name="Фото файл"
    )

    await show_layout_confirmation(
        message,
        state
    )


# =========================================================
# 📄 SAHIFALASH — FAYL YO‘Q
# =========================================================

@router.message(
    OrderStates.waiting_layout_file,
    F.text
)
async def get_layout_no_file(
    message: Message,
    state: FSMContext
):
    text = message.text.strip()

    if text.lower() in [
        "файл йўқ",
        "файл йок",
        "файл йўқ.",
        "файл йок.",
        "файл yo'q",
        "fayl yo'q",
        "fayl yoq"
    ]:
        await state.update_data(
            file_id=None,
            file_type=None,
            file_name=None
        )

        await show_layout_confirmation(
            message,
            state
        )
        return

    await message.answer(
        "⚠️ Илтимос, китоб файлини юборинг.\n\n"
        "📄 Word ёки PDF файл юборишингиз мумкин.\n\n"
        "Агар файл ҳозирча тайёр бўлмаса:\n"
        "<b>«Файл йўқ»</b> деб ёзинг.",
        reply_markup=order_cancel_menu(),
        parse_mode="HTML"
    )


# =========================================================
# 🔍 SAHIFALASH — TASDIQLASH
# =========================================================

async def show_layout_confirmation(
    message: Message,
    state: FSMContext
):
    data = await state.get_data()

    page_count = data.get("page_count", "Кўрсатилмаган")
    layout_format = data.get("layout_format", "Кўрсатилмаган")
    file_type = data.get("layout_file_type", "Кўрсатилмаган")
    design = data.get("layout_design", "Кўрсатилмаган")
    deadline = data.get("layout_deadline", "Кўрсатилмаган")
    file_name = data.get("file_name") or "Файл бириктирилмаган"

    text = (
        "🔍 <b>САҲИФАЛАШ БУЮРТМАСИ</b>\n\n"
        f"📑 <b>Хизмат:</b> {data.get('service')}\n"
        f"📄 <b>Бетлар сони:</b> {page_count}\n"
        f"📐 <b>Китоб формати:</b> {layout_format}\n"
        f"📎 <b>Манба файл тури:</b> {file_type}\n"
        f"🎨 <b>Дизайн талаби:</b> {design}\n"
        f"⏰ <b>Муддат:</b> {deadline}\n"
        f"📂 <b>Файл:</b> {file_name}\n\n"
        "Маълумотлар тўғри бўлса, "
        "<b>«Буюртмани тасдиқлаш»</b> тугмасини босинг."
    )

    await state.set_state(
        OrderStates.confirming
    )

    await message.answer(
        text,
        reply_markup=order_confirm_menu(),
        parse_mode="HTML"
    )
# =========================================================
# ❌ BUYURTMANI BEKOR QILISH
# =========================================================

@router.message(
    OrderStates.waiting_name,
    F.text == "❌ Буюртмани бекор қилиш"
)
@router.message(
    OrderStates.waiting_phone,
    F.text == "❌ Буюртмани бекор қилиш"
)
@router.message(
    OrderStates.waiting_service,
    F.text == "❌ Буюртмани бекор қилиш"
)
@router.message(
    OrderStates.waiting_task,
    F.text == "❌ Буюртмани бекор қилиш"
)
@router.message(
    OrderStates.waiting_volume,
    F.text == "❌ Буюртмани бекор қилиш"
)
@router.message(
    OrderStates.waiting_deadline,
    F.text == "❌ Буюртмани бекор қилиш"
)
@router.message(
    OrderStates.waiting_file,
    F.text == "❌ Буюртмани бекор қилиш"
)
async def cancel_order(
    message: Message,
    state: FSMContext
):
    await state.clear()

    await message.answer(
        "❌ <b>Буюртма бекор қилинди.</b>\n\n"
        "Истаган вақтингизда янги буюртма беришингиз мумкин.",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


# =========================================================
# 👤 ISM
# =========================================================

@router.message(OrderStates.waiting_name)
async def get_name(
    message: Message,
    state: FSMContext
):
    name = (message.text or "").strip()

    if len(name) < 3:
        await message.answer(
            "⚠️ Илтимос, исм ва фамилияни тўлиқ киритинг.\n\n"
            "Масалан: <i>Ахмаджонов Жалолиддин</i>",
            parse_mode="HTML"
        )
        return

    await state.update_data(
        name=name
    )

    await state.set_state(
        OrderStates.waiting_phone
    )

    await message.answer(
        "2️⃣ 📞 <b>Телефон рақамингизни юборинг:</b>\n\n"
        "Масалан: <i>+998 90 123 45 67</i>",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="📱 Телефон рақамимни юбориш",
                        request_contact=True
                    )
                ],
                [
                    KeyboardButton(
                        text="❌ Буюртмани бекор қилиш"
                    )
                ]
            ],
            resize_keyboard=True
        ),
        parse_mode="HTML"
    )


# =========================================================
# 📞 TELEFON — KONTAKT
# =========================================================

@router.message(
    OrderStates.waiting_phone,
    F.contact
)
async def get_phone_contact(
    message: Message,
    state: FSMContext
):
    phone = message.contact.phone_number

    await state.update_data(
        phone=phone
    )

    data = await state.get_data()
    selected_service = data.get("service")

    # Agar xizmat oldindan tanlangan bo‘lsa,
    # xizmat tanlash bosqichini o'tkazib yuboramiz
    if selected_service:
        await state.set_state(
            OrderStates.waiting_task
        )

        await message.answer(
            "4️⃣ 📝 <b>Мавзу ёки вазифани ёзинг:</b>\n\n"
            "Нима тайёрлаш кераклигини имкони борича аниқ ёзинг.\n\n"
            "Масалан:\n"
            "<i>7 бетлик тезис тайёрлаш керак. "
            "Мавзу: архитектурада замонавий технологиялар.</i>",
            reply_markup=order_cancel_menu(),
            parse_mode="HTML"
        )
        return

    # Агар хизмат олдиндан танланмаган бўлса,
    # одатдагидек хизмат танлашни сўраймиз
    await state.set_state(
        OrderStates.waiting_service
    )

    await message.answer(
        "3️⃣ 📚 <b>Қайси хизмат керак?</b>\n\n"
        "Керакли хизмат йўналишини танланг 👇",
        reply_markup=service_menu(),
        parse_mode="HTML"
    )

# =========================================================
# 📞 TELEFON — MATN
# =========================================================

@router.message(OrderStates.waiting_phone)
async def get_phone_text(
    message: Message,
    state: FSMContext
):
    phone = (message.text or "").strip()

    digits = "".join(
        ch for ch in phone
        if ch.isdigit()
    )

    if len(digits) < 9:
        await message.answer(
            "⚠️ Телефон рақами нотўғри кўринади.\n\n"
            "Илтимос, +998 билан тўлиқ рақам киритинг ёки "
            "📱 тугмаси орқали рақамингизни юборинг."
        )
        return

    await state.update_data(
        phone=phone
    )

    data = await state.get_data()
    selected_service = data.get("service")

    # Агар хизмат олдиндан танланган бўлса,
    # хизмат танлаш босқичини ўтказиб юборамиз
    if selected_service:
        await state.set_state(
            OrderStates.waiting_task
        )

        await message.answer(
            "4️⃣ 📝 <b>Мавзу ёки вазифани ёзинг:</b>\n\n"
            "Нима тайёрлаш кераклигини имкони борича аниқ ёзинг.\n\n"
            "Масалан:\n"
            "<i>7 бетлик тезис тайёрлаш керак. "
            "Мавзу: архитектурада замонавий технологиялар.</i>",
            reply_markup=order_cancel_menu(),
            parse_mode="HTML"
        )
        return

    # Агар хизмат олдиндан танланмаган бўлса,
    # одатдагидек хизмат танлашни сўраймиз
    await state.set_state(
        OrderStates.waiting_service
    )

    await message.answer(
        "3️⃣ 📚 <b>Қайси хизмат керак?</b>\n\n"
        "Керакли хизмат йўналишини танланг 👇",
        reply_markup=service_menu(),
        parse_mode="HTML"
    )

# =========================================================
# 📚 XIZMAT
# =========================================================

@router.message(OrderStates.waiting_service)
async def get_service(
    message: Message,
    state: FSMContext
):
    service = (message.text or "").strip()

    allowed_services = {
        "📚 Китоб ва нашриёт",
        "🎓 Илмий хизматлар",
        "🏆 Танлов ва лойиҳалар",
        "🎨 Дизайн ва медиа",
        "🌐 Сайт яратиш"
    }

    if service not in allowed_services:
        await message.answer(
            "⚠️ Илтимос, хизмат йўналишларидан "
            "бирини танланг 👇",
            reply_markup=service_menu()
        )
        return

    await state.update_data(
        service=service
    )

    await state.set_state(
        OrderStates.waiting_task
    )

    await message.answer(
        "4️⃣ 📝 <b>Мавзу ёки вазифани ёзинг:</b>\n\n"
        "Нима тайёрлаш кераклигини имкони борича аниқ ёзинг.\n\n"
        "Масалан:\n"
        "<i>7 бетлик илмий мақола тайёрлаш керак. "
        "Мавзу: архитектурада замонавий технологиялар.</i>",
        reply_markup=order_cancel_menu(),
        parse_mode="HTML"
    )


# =========================================================
# 📝 VAZIFA
# =========================================================

@router.message(OrderStates.waiting_task)
async def get_task(
    message: Message,
    state: FSMContext
):
    task = (message.text or "").strip()

    if len(task) < 5:
        await message.answer(
            "⚠️ Илтимос, вазифани батафсилроқ ёзинг."
        )
        return

    await state.update_data(
        task=task
    )

    await state.set_state(
        OrderStates.waiting_volume
    )

    await message.answer(
        "5️⃣ 📑 <b>Иш ҳажмини кўрсатинг:</b>\n\n"
        "Масалан:\n"
        "• 5 бет\n"
        "• 20 бет\n"
        "• 10 слайд\n"
        "• 1 та видео\n"
        "• 3 та дизайн",
        reply_markup=order_cancel_menu(),
        parse_mode="HTML"
    )


# =========================================================
# 📑 HAJM
# =========================================================

@router.message(OrderStates.waiting_volume)
async def get_volume(
    message: Message,
    state: FSMContext
):
    volume = (message.text or "").strip()

    if not volume:
        await message.answer(
            "⚠️ Илтимос, иш ҳажмини кўрсатинг."
        )
        return

    await state.update_data(
        volume=volume
    )

    await state.set_state(
        OrderStates.waiting_deadline
    )

    await message.answer(
        "6️⃣ ⏰ <b>Қачонга керак?</b>\n\n"
        "Аниқ сана ёки муддатни ёзинг.\n\n"
        "Масалан: <i>15 сентябргача</i>",
        reply_markup=order_cancel_menu(),
        parse_mode="HTML"
    )


# =========================================================
# ⏰ MUDDAT
# =========================================================

@router.message(OrderStates.waiting_deadline)
async def get_deadline(
    message: Message,
    state: FSMContext
):
    deadline = (message.text or "").strip()

    if len(deadline) < 2:
        await message.answer(
            "⚠️ Илтимос, топшириш муддатини кўрсатинг."
        )
        return

    await state.update_data(
        deadline=deadline
    )

    await state.set_state(
        OrderStates.waiting_file
    )

    await message.answer(
        "7️⃣ 📎 <b>Файл ёки намуна борми?</b>\n\n"
        "Агар бўлса, ҳозир юборинг.\n"
        "PDF, Word, Excel, расм ёки бошқа файл "
        "юборишингиз мумкин.\n\n"
        "Агар файл бўлмаса, "
        "<b>Файл йўқ</b> тугмасини босинг.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="📭 Файл йўқ"
                    )
                ],
                [
                    KeyboardButton(
                        text="❌ Буюртмани бекор қилиш"
                    )
                ]
            ],
            resize_keyboard=True
        ),
        parse_mode="HTML"
    )


# =========================================================
# 📎 HUJJAT
# =========================================================

@router.message(
    OrderStates.waiting_file,
    F.document
)
async def get_document(
    message: Message,
    state: FSMContext
):
    document = message.document

    await state.update_data(
        file_type="document",
        file_id=document.file_id,
        file_name=document.file_name or "Файл"
    )

    await show_order_confirmation(
        message,
        state
    )


# =========================================================
# 🖼 RASM
# =========================================================

@router.message(
    OrderStates.waiting_file,
    F.photo
)
async def get_photo(
    message: Message,
    state: FSMContext
):
    photo = message.photo[-1]

    await state.update_data(
        file_type="photo",
        file_id=photo.file_id,
        file_name="Расм"
    )

    await show_order_confirmation(
        message,
        state
    )


# =========================================================
# 📭 FAYL YO‘Q
# =========================================================

@router.message(
    OrderStates.waiting_file,
    F.text == "📭 Файл йўқ"
)
async def no_file(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        file_type="none",
        file_id=None,
        file_name=None
    )

    await show_order_confirmation(
        message,
        state
    )


# =========================================================
# ⚠️ NOTO‘G‘RI FAYL
# =========================================================

@router.message(OrderStates.waiting_file)
async def invalid_file(
    message: Message
):
    await message.answer(
        "⚠️ Илтимос, файл ёки расм юборинг.\n\n"
        "Агар файл бўлмаса, "
        "<b>📭 Файл йўқ</b> тугмасини босинг.",
        parse_mode="HTML"
    )


# =========================================================
# 🔍 BUYURTMA TASDIQLASH OYNASI
# =========================================================

async def show_order_confirmation(
    message: Message,
    state: FSMContext
):
    data = await state.get_data()

    file_name = (
        data.get("file_name")
        or "Файл бириктирилмаган"
    )

    text = (
        "🔍 <b>БУЮРТМА МАЪЛУМОТЛАРИ</b>\n\n"
        f"👤 <b>Мижоз:</b> {data.get('name')}\n"
        f"📞 <b>Телефон:</b> {data.get('phone')}\n"
        f"📚 <b>Хизмат:</b> {data.get('service')}\n"
        f"📝 <b>Вазифа:</b> {data.get('task')}\n"
        f"📑 <b>Ҳажм:</b> {data.get('volume') or data.get('page_count', '—')}\n"
        f"📄 <b>Бетлар сони:</b> {data.get('page_count', '—')}\n"
        f"📐 <b>Формат:</b> {data.get('layout_format', '—')}\n"
        f"📎 <b>Файл тури:</b> {data.get('layout_file_type', '—')}\n"
        f"🎨 <b>Дизайн:</b> {data.get('layout_design', '—')}\n"
        f"⏰ <b>Муддат:</b> {data.get('deadline') or data.get('layout_deadline', '—')}\n"
        f"📎 <b>Файл:</b> {file_name}\n\n"
        "Маълумотлар тўғри бўлса, "
        "тасдиқланг 👇"
    )

    await state.set_state(
        OrderStates.confirming
    )

    await message.answer(
        text,
        reply_markup=order_confirm_menu(),
        parse_mode="HTML"
    )


# =========================================================
# ✏️ MA'LUMOTNI O‘ZGARTIRISH
# =========================================================

@router.message(
    OrderStates.confirming,
    F.text == "✏️ Маълумотни ўзгартириш"
)
async def edit_order(
    message: Message,
    state: FSMContext
):
    await state.clear()

    await state.set_state(
        OrderStates.waiting_name
    )

    await message.answer(
        "✏️ <b>Маълумотларни қайта киритиш</b>\n\n"
        "1️⃣ 👤 Исм ва фамилиянгизни киритинг:",
        reply_markup=order_cancel_menu(),
        parse_mode="HTML"
    )


# =========================================================
# ❌ TASDIQLASHDAN OLDIN BEKOR QILISH
# =========================================================

@router.message(
    OrderStates.confirming,
    F.text == "❌ Бекор қилиш"
)
async def cancel_confirmed_order(
    message: Message,
    state: FSMContext
):
    await state.clear()

    await message.answer(
        "❌ <b>Буюртма бекор қилинди.</b>\n\n"
        "Бош менюдан истаган вақтингизда "
        "янги буюртма беришингиз мумкин.",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


# =========================================================
# ✅ BUYURTMANI TASDIQLASH VA BAZAGA SAQLASH
# =========================================================

@router.message(
    OrderStates.confirming,
    F.text == "✅ Буюртмани тасдиқлаш"
)
async def confirm_order(
    message: Message,
    state: FSMContext
):
    data = await state.get_data()

    username = (
        f"@{message.from_user.username}"
        if message.from_user.username
        else "Username мавжуд эмас"
    )

    order_number = (
        f"OA-"
        f"{datetime.now().strftime('%Y%m%d%H%M%S')}-"
        f"{uuid.uuid4().hex[:4].upper()}"
    )

    try:

        # =================================================
        # 🗄️ BUYURTMANI BAZAGA SAQLASH
        # =================================================

        async with async_session() as session:

            new_order = Order(
                order_number=order_number,
                user_id=message.from_user.id,
                username=message.from_user.username,
                name=data.get("name"),
                phone=data.get("phone"),
                service=data.get("service"),
                task=(
    data.get("task")
    or (
        f"Саҳифалар: {data.get('page_count', 'Кўрсатилмаган')}; "
        f"Формат: {data.get('layout_format', 'Кўрсатилмаган')}; "
        f"Файл тури: {data.get('layout_file_type', 'Кўрсатилмаган')}; "
        f"Дизайн: {data.get('layout_design', 'Кўрсатилмаган')}"
    )
),
                volume=data.get("volume"),
                deadline=data.get("deadline"),
                file_id=data.get("file_id"),
                file_type=data.get("file_type"),
                file_name=data.get("file_name"),
                status="new",
                created_at=datetime.now()
            )

            session.add(new_order)

            await session.commit()

        # =================================================
        # 📩 ADMINGA BUYURTMA
        # =================================================

        admin_text = (
            "🔔 <b>ЯНГИ БУЮРТМА!</b>\n\n"
            f"🆔 <b>Буюртма рақами:</b> {order_number}\n"
            f"👤 <b>Мижоз:</b> {data.get('name')}\n"
            f"📞 <b>Телефон:</b> {data.get('phone')}\n"
            f"📚 <b>Хизмат:</b> {data.get('service')}\n"
            f"📝 <b>Мавзу/вазифа:</b> {data.get('task')}\n"
            f"📑 <b>Ҳажм:</b> {data.get('volume')}\n"
            f"⏰ <b>Муддат:</b> {data.get('deadline')}\n"
            f"📎 <b>Файл:</b> "
            f"{data.get('file_name') or 'Йўқ'}\n"
            f"💬 <b>Telegram:</b> {username}\n"
            f"🆔 <b>User ID:</b> {message.from_user.id}\n"
            f"🔄 <b>Статус:</b> 🆕 Янги"
        )

        await message.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_text,
            parse_mode="HTML"
        )

        # =================================================
        # 📎 FAYLNI ADMINGA YUBORISH
        # =================================================

        if (
            data.get("file_type") == "document"
            and data.get("file_id")
        ):
            await message.bot.send_document(
                chat_id=ADMIN_ID,
                document=data["file_id"],
                caption=(
                    f"📎 {order_number} — "
                    "Буюртма файли"
                )
            )

        elif (
            data.get("file_type") == "photo"
            and data.get("file_id")
        ):
            await message.bot.send_photo(
                chat_id=ADMIN_ID,
                photo=data["file_id"],
                caption=(
                    f"📎 {order_number} — "
                    "Буюртма расми"
                )
            )

        # =================================================
        # ✅ MIJOZGA TASDIQ
        # =================================================

        await message.answer(
            "☑️ <b>Буюртмангиз қабул қилинди!</b>\n\n"
            f"🆔 <b>Буюртма рақами:</b> "
            f"{order_number}\n\n"
            "Маълумотларингиз сақланди ва "
            "администраторга юборилди.\n"
            "Мутахассисимиз буюртмани кўриб чиқиб, "
            "сиз билан боғланади.\n\n"
            "<b>ORZU AKADEMIYA</b>ни "
            "танлаганингиз учун ташаккур! 🌷",
            reply_markup=main_menu(),
            parse_mode="HTML"
        )

        await state.clear()

    except Exception as e:

        print(
            f"❌ Буюртмани сақлашда хато: {e}"
        )

        await message.answer(
            "⚠️ <b>Буюртмани сақлашда "
            "техник муаммо юз берди.</b>\n\n"
            "Илтимос, бироздан сўнг "
            "қайта уриниб кўринг.",
            reply_markup=main_menu(),
            parse_mode="HTML"
        )


# =========================================================
# ⚠️ TASDIQLASHDA NOTO‘G‘RI XABAR
# =========================================================

@router.message(OrderStates.confirming)
async def invalid_confirmation(
    message: Message
):
    await message.answer(
        "⚠️ Илтимос, қуйидаги тугмалардан "
        "бирини танланг 👇",
        reply_markup=order_confirm_menu()
    )