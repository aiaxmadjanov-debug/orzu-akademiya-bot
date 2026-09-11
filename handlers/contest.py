from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from keyboards.contest_menu import contest_menu
from keyboards.main_menu import main_menu


router = Router()


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


@router.message(F.text == "🏆 Танлов ва лойиҳалар")
async def contest_menu_handler(message: Message):
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


@router.message(F.text == "🔥 Жорий танловлар")
async def current_contests(message: Message):
    await message.answer(
        "🔥 <b>ЖОРИЙ ТАНЛОВЛАР</b>\n\n"
        "Ҳозирги танловлар ҳақида тўлиқ маълумот:\n\n"
        "📌 <b>Танлов номи:</b>\n"
        "Ҳозирча маълумот киритилмаган.\n\n"
        "📌 <b>Қатнашиш шартлари:</b>\n"
        "Танлов шартлари администратор томонидан янгиланади.\n\n"
        "📌 <b>Қабул муддати:</b>\n"
        "Маълумот кейинроқ киритилади.\n\n"
        "📌 <b>Мукофотлар:</b>\n"
        "Мукофотлар ҳақида маълумот танлов эълон қилинганда берилади.\n\n"
        "📌 <b>Иштирок этиш тартиби:</b>\n"
        "📝 Иштирок этиш тугмасини босинг ва маълумотларингизни қолдиринг.",
        reply_markup=contest_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "🏅 Миллат Ғурури")
async def millat_gururi(message: Message):
    await message.answer(
        "🏅 <b>МИЛЛАТ ҒУРУРИ</b>\n\n"
        "Миллий қадриятлар, илм-фан, ижод ва жамият "
        "ривожига ҳисса қўшаётган иштирокчиларни қўллаб-қувватлашга "
        "қаратилган лойиҳа.\n\n"
        "📌 Танлов шартлари\n"
        "📌 Иштирок этиш тартиби\n"
        "📌 Қабул муддати\n"
        "📌 Мукофотлар\n\n"
        "📝 Иштирок этиш учун қуйидаги тугмани босинг.",
        reply_markup=contest_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "🏆 Шифо Элчиси")
async def shifo_elchisi(message: Message):
    await message.answer(
        "🏆 <b>ШИФО ЭЛЧИСИ</b>\n\n"
        "Соғлом турмуш тарзи, тиббий маданият ва жамиятда "
        "фойдали ташаббусларни қўллаб-қувватлашга қаратилган лойиҳа.\n\n"
        "📌 Қатнашиш шартлари\n"
        "📌 Иштирок тартиби\n"
        "📌 Қабул муддати\n"
        "📌 Мукофотлар\n\n"
        "📝 Иштирок этиш учун қуйидаги тугмани босинг.",
        reply_markup=contest_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "🧠 Онг ва Шифо")
async def ong_va_shifo(message: Message):
    await message.answer(
        "🧠 <b>ОНГ ВА ШИФО</b>\n\n"
        "Инсон тафаккури, маънавий ривожланиш ва ижтимоий "
        "фойдали ғояларни илгари суришга қаратилган лойиҳа.\n\n"
        "📌 Танлов йўналиши\n"
        "📌 Қатнашиш шартлари\n"
        "📌 Қабул муддати\n"
        "📌 Мукофотлар\n\n"
        "📝 Иштирок этиш учун қуйидаги тугмани босинг.",
        reply_markup=contest_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "🌷 Азизим Онам")
async def azizim_onam(message: Message):
    await message.answer(
        "🌷 <b>АЗИЗИМ ОНАМ</b>\n\n"
        "Онажонларга бағишланган ижодий ва маънавий лойиҳа.\n\n"
        "📌 Иштирок шартлари\n"
        "📌 Қабул муддати\n"
        "📌 Иштирок этиш тартиби\n"
        "📌 Мукофотлар\n\n"
        "📝 Иштирок этиш учун қуйидаги тугмани босинг.",
        reply_markup=contest_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "📚 Илмий мақола танловлари")
async def scientific_contests(message: Message):
    await message.answer(
        "📚 <b>ИЛМИЙ МАҚОЛА ТАНЛОВЛАРИ</b>\n\n"
        "Илмий мақола ва тадқиқот ишлари бўйича танловлар.\n\n"
        "☑️ Илмий мақола\n"
        "☑️ Тадқиқот натижалари\n"
        "☑️ Илмий-ижодий ишлар\n"
        "☑️ Мукофот ва сертификатлар\n\n"
        "📌 Амалдаги танлов шартлари администратор томонидан "
        "янгиланиб борилади.\n\n"
        "📝 Иштирок этиш учун қуйидаги тугмани босинг.",
        reply_markup=contest_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "📝 Иштирок этиш")
async def participate(message: Message):
    await message.answer(
        "📝 <b>ТАНЛОВДА ИШТИРОК ЭТИШ</b>\n\n"
        "Иштирок этиш учун қуйидаги маълумотларни тайёрланг:\n\n"
        "👤 Исм ва фамилия\n"
        "📞 Телефон рақами\n"
        "🏆 Танлов номи\n"
        "📝 Иш ёки лойиҳа ҳақида маълумот\n"
        "📎 Зарур файллар\n\n"
        "Маълумотларингиз қабул қилингач, "
        "администратор сиз билан боғланади. 📩\n\n"
        "⚙️ <i>Иштирок этиш формаси кейинги босқичда автоматлаштирилади.</i>",
        reply_markup=contest_service_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "⬅️ Танловлар")
async def back_to_contests(message: Message):
    await message.answer(
        "🏆 <b>ТАНЛОВ ВА ЛОЙИҲАЛАР</b>\n\n"
        "Керакли бўлимни танланг 👇",
        reply_markup=contest_menu(),
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