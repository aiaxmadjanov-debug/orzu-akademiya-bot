from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext

from keyboards.contest_menu import contest_menu
from keyboards.main_menu import main_menu
from states.contest_states import ContestStates
from config import ADMIN_ID


router = Router()


# =========================================================
# 🏆 TANLOV ICHKI MENYUSI
# =========================================================

def contest_service_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📝 Иштирок этиш")
            ],
            [
                KeyboardButton(text="⬅️ Танловлар")
            ],
            [
                KeyboardButton(text="🏠 Бош меню")
            ]
        ],
        resize_keyboard=True
    )


# =========================================================
# 🏆 TANLOV VA LOYIHALAR
# =========================================================

@router.message(F.text == "🏆 Танлов ва лойиҳалар")
async def contest_menu_handler(message: Message):

    await message.answer(
        "🏆 <b>ТАНЛОВ ВА ЛОЙИҲАЛАР</b>\n\n"
        "Керакли бўлимни танланг 👇",
        reply_markup=contest_menu(),
        parse_mode="HTML"
    )


# =========================================================
# 🔥 JORIY TANLOVLAR
# =========================================================

@router.message(F.text == "🔥 Жорий танловлар")
async def current_contests(message: Message):

    await message.answer(
        "🔥 <b>ЖОРИЙ ТАНЛОВЛАР</b>\n\n"
        "Ҳозирги танловлар ҳақида маълумот.\n\n"
        "📝 Иштирок этиш учун қуйидаги тугмани босинг.",
        reply_markup=contest_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 🏅 MILLAT GURURI
# =========================================================

@router.message(F.text == "🏅 Миллат Ғурури")
async def millat_gururi(message: Message):

    await message.answer(
        "🏅 <b>МИЛЛАТ ҒУРУРИ</b>\n\n"
        "Миллий қадриятлар, илм-фан, ижод ва жамият "
        "ривожига ҳисса қўшаётган иштирокчиларни "
        "қўллаб-қувватлашга қаратилган лойиҳа.\n\n"
        "📝 Иштирок этиш учун қуйидаги тугмани босинг.",
        reply_markup=contest_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 🏆 SHIFO ELCHISI
# =========================================================

@router.message(F.text == "🏆 Шифо Элчиси")
async def shifo_elchisi(message: Message):

    await message.answer(
        "🏆 <b>ШИФО ЭЛЧИСИ</b>\n\n"
        "Соғлом турмуш тарзи, тиббий маданият ва "
        "жамиятда фойдали ташаббусларни қўллаб-қувватлашга "
        "қаратилган лойиҳа.\n\n"
        "📝 Иштирок этиш учун қуйидаги тугмани босинг.",
        reply_markup=contest_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 🧠 ONG VA SHIFO
# =========================================================

@router.message(F.text == "🧠 Онг ва Шифо")
async def ong_va_shifo(message: Message):

    await message.answer(
        "🧠 <b>ОНГ ВА ШИФО</b>\n\n"
        "Инсон тафаккури, маънавий ривожланиш ва "
        "ижтимоий фойдали ғояларни илгари суришга "
        "қаратилган лойиҳа.\n\n"
        "📝 Иштирок этиш учун қуйидаги тугмани босинг.",
        reply_markup=contest_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 🌷 AZIZIM ONAM
# =========================================================

@router.message(F.text == "🌷 Азизим Онам")
async def azizim_onam(message: Message):

    await message.answer(
        "🌷 <b>АЗИЗИМ ОНАМ</b>\n\n"
        "Онажонларга бағишланган ижодий ва маънавий лойиҳа.\n\n"
        "📝 Иштирок этиш учун қуйидаги тугмани босинг.",
        reply_markup=contest_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 📚 ILMIY MAQOLA
# =========================================================

@router.message(F.text == "📚 Илмий мақола танловлари")
async def scientific_contests(message: Message):

    await message.answer(
        "📚 <b>ИЛМИЙ МАҚОЛА ТАНЛОВЛАРИ</b>\n\n"
        "Илмий мақола ва тадқиқот ишлари бўйича танловлар.\n\n"
        "📝 Иштирок этиш учун қуйидаги тугмани босинг.",
        reply_markup=contest_service_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 🏆 E'TIROF 2026
# =========================================================

@router.message(
    ContestStates.waiting_contest,
    F.text == "🏆 Эътироф — 2026"
)
async def contest_get_contest(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        contest="Эътироф — 2026"
    )

    await state.set_state(
        ContestStates.waiting_description
    )

    await message.answer(
        "4️⃣ 📝 <b>ЎЗИНГИЗ ҲАҚИНГИЗДА</b>\n\n"
        "Касбингиз, лавозимингиз ва фаолиятингиз "
        "ҳақида қисқача ёзинг.\n\n"
        "Масалан:\n"
        "<i>Мен архитекторман. 5 йилдан бери "
        "архитектура соҳасида фаолият юритаман.</i>",
        parse_mode="HTML"
    )
@router.message(F.text == "🏆 Эътироф — 2026")
async def etirof_2026(
    message: Message,
    state: FSMContext
):
    await state.clear()

    await state.set_state(
        ContestStates.waiting_name
    )

    await message.answer(
        "🏆 <b>E’TİROF — 2026</b>\n\n"
        "📝 <b>Иштирок этиш учун маълумотларни киритинг.</b>\n\n"
        "1️⃣ 👤 <b>Исм ва фамилиянгизни киритинг:</b>\n\n"
        "Масалан:\n"
        "<i>Ахмаджонов Жалолиддин</i>",
        parse_mode="HTML"
    )
# =========================================================
# 📝 ISHTIROK ETISH
# =========================================================

@router.message(F.text == "📝 Иштирок этиш")
async def participate(
    message: Message,
    state: FSMContext
):

    await state.clear()

    await state.set_state(
        ContestStates.waiting_name
    )

    await message.answer(
        "🏆 <b>E’TİROF — 2026</b>\n\n"
        "📝 Иштирок этиш учун маълумотларни киритинг.\n\n"
        "1️⃣ 👤 <b>Исм ва фамилиянгизни киритинг:</b>\n\n"
        "Масалан:\n"
        "<i>Ахмаджонов Жалолиддин</i>",
        parse_mode="HTML"
    )


# =========================================================
# 👤 ISM VA FAMILIYA
# =========================================================

@router.message(ContestStates.waiting_name)
async def contest_get_name(
    message: Message,
    state: FSMContext
):

    name = (message.text or "").strip()

    if len(name) < 3:
        await message.answer(
            "⚠️ Илтимос, исм ва фамилияни тўлиқ киритинг.\n\n"
            "Масалан:\n"
            "<i>Ахмаджонов Жалолиддин</i>",
            parse_mode="HTML"
        )
        return

    await state.update_data(
        name=name
    )

    await state.set_state(
        ContestStates.waiting_phone
    )

    await message.answer(
        "2️⃣ 📞 <b>Телефон рақамингизни юборинг:</b>\n\n"
        "Пастдаги тугмани босинг 👇",
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
                        text="❌ Бекор қилиш"
                    )
                ]
            ],
            resize_keyboard=True
        ),
        parse_mode="HTML"
    )


# =========================================================
# 📞 TELEFON — CONTACT
# =========================================================

@router.message(
    ContestStates.waiting_phone,
    F.contact
)
async def contest_get_phone_contact(
    message: Message,
    state: FSMContext
):

    phone = message.contact.phone_number

    await state.update_data(
        phone=phone
    )

    await state.set_state(
        ContestStates.waiting_contest
    )

    await message.answer(
        "3️⃣ 🏆 <b>ТАНЛОВНИ ТАНЛАНГ:</b>\n\n"
        "Сиз иштирок этаётган танлов:\n\n"
        "🏆 <b>Эътироф — 2026</b>\n\n"
        "Қуйидаги тугмани босинг 👇",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="🏆 Эътироф — 2026"
                    )
                ],
                [
                    KeyboardButton(
                        text="❌ Бекор қилиш"
                    )
                ]
            ],
            resize_keyboard=True
        ),
        parse_mode="HTML"
    )


# =========================================================
# 📞 TELEFON — MATN
# =========================================================

@router.message(
    ContestStates.waiting_phone
)
async def contest_get_phone_text(
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
            "⚠️ <b>Телефон рақами нотўғри.</b>\n\n"
            "📱 Пастдаги тугмани босиб телефон рақамингизни "
            "юборинг.",
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
                            text="❌ Бекор қилиш"
                        )
                    ]
                ],
                resize_keyboard=True
            ),
            parse_mode="HTML"
        )
        return

    await state.update_data(
        phone=phone
    )

    await state.set_state(
        ContestStates.waiting_contest
    )

    await message.answer(
        "3️⃣ 🏆 <b>ТАНЛОВНИ ТАНЛАНГ:</b>\n\n"
        "Сиз иштирок этаётган танлов:\n\n"
        "🏆 <b>Эътироф — 2026</b>\n\n"
        "Қуйидаги тугмани босинг 👇",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="🏆 Эътироф — 2026"
                    )
                ],
                [
                    KeyboardButton(
                        text="❌ Бекор қилиш"
                    )
                ]
            ],
            resize_keyboard=True
        ),
        parse_mode="HTML"
    )


# =========================================================
# 🏆 TANLOV
# =========================================================

@router.message(
    ContestStates.waiting_contest,
    F.text == "🏆 Эътироф — 2026"
)
async def contest_get_contest(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        contest="Эътироф — 2026"
    )

    await state.set_state(
        ContestStates.waiting_description
    )

    await message.answer(
        "4️⃣ 📝 <b>ЎЗИНГИЗ ҲАҚИНГИЗДА</b>\n\n"
        "Касбингиз, лавозимингиз ва фаолиятингиз "
        "ҳақида қисқача ёзинг.\n\n"
        "Масалан:\n"
        "<i>Мен архитекторман. 5 йилдан бери "
        "архитектура соҳасида фаолият юритаман.</i>",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="❌ Бекор қилиш"
                    )
                ]
            ],
            resize_keyboard=True
        ),
        parse_mode="HTML"
    )


# =========================================================
# 📝 FAOLIYAT
# =========================================================

@router.message(
    ContestStates.waiting_description
)
async def contest_get_description(
    message: Message,
    state: FSMContext
):

    description = (message.text or "").strip()

    if len(description) < 10:
        await message.answer(
            "⚠️ Илтимос, ўзингиз ҳақингизда батафсилроқ ёзинг."
        )
        return

    await state.update_data(
        description=description
    )

    await state.set_state(
        ContestStates.waiting_file
    )

    await message.answer(
    "5️⃣ 📎 <b>ФАЙЛ ЁКИ ИШ НАМУНАСИ</b>\n\n"
    "Агар диплом, сертификат, расм, мақола ёки бошқа "
    "иш намунаси бўлса, шу ерга юборинг.\n\n"
    "Агар файл бўлмаса, қуйидаги тугмани босинг 👇",
    reply_markup=ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📭 Файл йўқ")
            ],
            [
                KeyboardButton(text="❌ Бекор қилиш")
            ]
        ],
        resize_keyboard=True
    ),
    parse_mode="HTML"
)


# =========================================================
# 📎 DOCUMENT
# =========================================================

@router.message(
    ContestStates.waiting_file,
    F.document
)
async def contest_get_document(
    message: Message,
    state: FSMContext
):

    document = message.document

    await state.update_data(
        file_type="document",
        file_id=document.file_id,
        file_name=document.file_name or "Файл"
    )

    await contest_finish(
        message,
        state
    )


# =========================================================
# 🖼 PHOTO
# =========================================================

@router.message(
    ContestStates.waiting_file,
    F.photo
)
async def contest_get_photo(
    message: Message,
    state: FSMContext
):

    photo = message.photo[-1]

    await state.update_data(
        file_type="photo",
        file_id=photo.file_id,
        file_name="Расм"
    )

    await contest_finish(
        message,
        state
    )


# =========================================================
# 📭 FILE YO'Q
# =========================================================

@router.message(
    ContestStates.waiting_file,
    F.text == "📭 Файл йўқ"
)
async def contest_no_file(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        file_type="none",
        file_id=None,
        file_name=None
    )

    await contest_finish(
        message,
        state
    )

# =========================================================
# 🔍 TASDIQLASH OYNASI
# =========================================================

async def contest_finish(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()

    text = (
        "🔍 <b>АРИЗА МАЪЛУМОТЛАРИ</b>\n\n"
        f"👤 <b>Исм:</b> {data.get('name')}\n"
        f"📞 <b>Телефон:</b> {data.get('phone')}\n"
        f"🏆 <b>Танлов:</b> {data.get('contest')}\n"
        f"📝 <b>Маълумот:</b> {data.get('description')}\n"
        f"📎 <b>Файл:</b> {data.get('file_name') or 'Йўқ'}\n\n"
        "Маълумотлар тўғри бўлса, тасдиқланг 👇"
    )

    await state.set_state(
        ContestStates.confirming
    )

    await message.answer(
        text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="✅ Тасдиқлаш"
                    )
                ],
                [
                    KeyboardButton(
                        text="❌ Бекор қилиш"
                    )
                ]
            ],
            resize_keyboard=True
        ),
        parse_mode="HTML"
    )


# =========================================================
# ✅ TASDIQLASH VA ADMINGA YUBORISH
# =========================================================

@router.message(
    ContestStates.confirming,
    F.text == "✅ Тасдиқлаш"
)
async def confirm_contest(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()

    username = (
        f"@{message.from_user.username}"
        if message.from_user.username
        else "Username мавжуд эмас"
    )

    admin_text = (
        "🔔 <b>ЯНГИ E’TİROF — 2026 АРИЗАСИ!</b>\n\n"
        f"👤 <b>Исм:</b> {data.get('name')}\n"
        f"📞 <b>Телефон:</b> {data.get('phone')}\n"
        f"🏆 <b>Танлов:</b> {data.get('contest')}\n"
        f"📝 <b>Маълумот:</b>\n{data.get('description')}\n\n"
        f"📎 <b>Файл:</b> {data.get('file_name') or 'Йўқ'}\n"
        f"💬 <b>Telegram:</b> {username}\n"
        f"🆔 <b>User ID:</b> {message.from_user.id}"
    )

    try:

        await message.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_text,
            parse_mode="HTML"
        )

        if data.get("file_type") == "document":

            await message.bot.send_document(
                chat_id=ADMIN_ID,
                document=data["file_id"],
                caption="📎 E’TİROF — 2026 файли"
            )

        elif data.get("file_type") == "photo":

            await message.bot.send_photo(
                chat_id=ADMIN_ID,
                photo=data["file_id"],
                caption="📎 E’TİROF — 2026 расми"
            )

        await message.answer(
            "✅ <b>Аризангиз муваффақиятли юборилди!</b>\n\n"
            "Маълумотларингиз администраторга юборилди. 📩\n\n"
            "Ташкилотчилар маълумотларингизни кўриб чиқиб, "
            "зарур бўлса сиз билан боғланади.",
            reply_markup=main_menu(),
            parse_mode="HTML"
        )

        await state.clear()

    except Exception as e:

        print(
            f"❌ E’TİROF юборишда хато: {e}"
        )

        await message.answer(
            "⚠️ <b>Аризани юборишда техник муаммо юз берди.</b>\n\n"
            "Илтимос, бироздан сўнг қайта уриниб кўринг.",
            reply_markup=main_menu(),
            parse_mode="HTML"
        )


# =========================================================
# ❌ BEKOR QILISH
# =========================================================

@router.message(
    F.text == "❌ Бекор қилиш"
)
async def cancel_contest(
    message: Message,
    state: FSMContext
):

    await state.clear()

    await message.answer(
        "❌ <b>Иштирок этиш бекор қилинди.</b>",
        reply_markup=contest_menu(),
        parse_mode="HTML"
    )


# =========================================================
# ⬅️ TANLOVLAR
# =========================================================

@router.message(F.text == "⬅️ Танловлар")
async def back_to_contests(message: Message):

    await message.answer(
        "🏆 <b>ТАНЛОВ ВА ЛОЙИҲАЛАР</b>\n\n"
        "Керакли бўлимни танланг 👇",
        reply_markup=contest_menu(),
        parse_mode="HTML"
    )


# =========================================================
# 🏠 BOSH MENU
# =========================================================

@router.message(F.text == "🏠 Бош меню")
async def back_to_main(message: Message):

    await message.answer(
        "🏠 <b>Бош меню</b>\n\n"
        "Керакли бўлимни танланг 👇",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )