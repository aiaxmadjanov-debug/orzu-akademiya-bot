from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def contest_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🔥 Жорий танловлар")
            ],
            [
                KeyboardButton(text="🏅 Миллат Ғурури"),
                KeyboardButton(text="🏆 Шифо Элчиси")
            ],
            [
                KeyboardButton(text="🧠 Онг ва Шифо"),
                KeyboardButton(text="🌷 Азизим Онам")
            ],
            [
                KeyboardButton(text="📚 Илмий мақола танловлари")
            ],
            [
                KeyboardButton(text="🏆 Эътироф — 2026")
            ],
            [
                KeyboardButton(text="📝 Иштирок этиш")
            ],
            [
                KeyboardButton(text="⬅️ Бош меню")
            ]
        ],
        resize_keyboard=True
    )