from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def scientific_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📄 Илмий мақола"),
                KeyboardButton(text="📝 Тезис")
            ],
            [
                KeyboardButton(text="📚 Монография"),
                KeyboardButton(text="🎓 Магистрлик иши")
            ],
            [
                KeyboardButton(text="🌍 Халқаро мақола"),
                KeyboardButton(text="📊 Тақдимот")
            ],
            [
                KeyboardButton(text="🔎 Плагиат текшируви"),
                KeyboardButton(text="📑 Манбалар ва адабиётлар")
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