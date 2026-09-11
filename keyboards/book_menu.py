from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def book_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📖 Китоб ёзиш"),
                KeyboardButton(text="✍️ Матн таҳрири")
            ],
            [
                KeyboardButton(text="📝 Корректура"),
                KeyboardButton(text="🎨 Муқова дизайни")
            ],
            [
                KeyboardButton(text="📑 Саҳифалаш"),
                KeyboardButton(text="🔎 Плагиат текшируви")
            ],
            [
                KeyboardButton(text="🔢 ISBN"),
                KeyboardButton(text="📚 Монография")
            ],
            [
                KeyboardButton(text="🌍 Amazon KDP"),
                KeyboardButton(text="🇬🇧 Таржима")
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