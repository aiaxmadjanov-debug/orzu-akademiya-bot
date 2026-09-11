from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def website_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🌐 Шахсий сайт"),
                KeyboardButton(text="🏢 Компания сайти")
            ],
            [
                KeyboardButton(text="📚 Муаллиф сайти"),
                KeyboardButton(text="🛍 Хизматлар сайти")
            ],
            [
                KeyboardButton(text="📱 Телефонга мос дизайн"),
                KeyboardButton(text="💬 Telegram ва Instagram")
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