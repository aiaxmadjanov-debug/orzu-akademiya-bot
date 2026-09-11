from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
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
                KeyboardButton(text="🌐 Сайт яратиш"),
                KeyboardButton(text="💰 Нархлар")
            ],
            [
                KeyboardButton(text="🔥 Акциялар"),
                KeyboardButton(text="📝 Буюртма бериш")
            ],
            [
                KeyboardButton(text="⭐️ Бизнинг ишлар"),
                KeyboardButton(text="🤖 Қайси хизмат керак?")
            ],
            [
                KeyboardButton(text="☎️ Админ билан боғланиш")
            ]
        ],
        resize_keyboard=True
    )