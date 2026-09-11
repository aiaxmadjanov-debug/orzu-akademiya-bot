from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📝 Буюртмалар"),
                KeyboardButton(text="👥 Фойдаланувчилар")
            ],
            [
                KeyboardButton(text="📊 Статистика"),
                KeyboardButton(text="📢 Рассылка")
            ],
            [
                KeyboardButton(text="💰 Нархларни бошқариш"),
                KeyboardButton(text="🔥 Акцияларни бошқариш")
            ],
            [
                KeyboardButton(text="⭐️ Ишларни бошқариш"),
                KeyboardButton(text="⚙️ Созламалар")
            ],
            [
                KeyboardButton(text="🏠 Асосий меню")
            ]
        ],
        resize_keyboard=True
    )