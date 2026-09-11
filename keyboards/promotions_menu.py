from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def promotions_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🔥 Жорий акциялар")
            ],
            [
                KeyboardButton(text="🎁 Бонуслар"),
                KeyboardButton(text="⏰ Муддатли таклифлар")
            ],
            [
                KeyboardButton(text="📚 Китоб нашри акциялари")
            ],
            [
                KeyboardButton(text="🎓 Илмий хизматлар акциялари")
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