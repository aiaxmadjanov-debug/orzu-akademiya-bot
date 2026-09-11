from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def design_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🎨 Логотип"),
                KeyboardButton(text="📜 Сертификат / диплом")
            ],
            [
                KeyboardButton(text="📢 Реклама пост"),
                KeyboardButton(text="🎬 Reels")
            ],
            [
                KeyboardButton(text="🤖 AI видео"),
                KeyboardButton(text="🎤 Диктор овози")
            ],
            [
                KeyboardButton(text="📚 Китоб рекламаси")
            ],
            [
                KeyboardButton(text="📝 Буюртма бериш")
            ],
            [
                KeyboardButton(text="⬅️ Бош меню")
            ]
        ],
        resize_keyboard=True
    )