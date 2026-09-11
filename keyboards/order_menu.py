from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def order_cancel_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="❌ Буюртмани бекор қилиш"
                )
            ]
        ],
        resize_keyboard=True
    )


def order_confirm_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="✅ Буюртмани тасдиқлаш"
                )
            ],
            [
                KeyboardButton(
                    text="✏️ Маълумотни ўзгартириш"
                )
            ],
            [
                KeyboardButton(
                    text="❌ Бекор қилиш"
                )
            ]
        ],
        resize_keyboard=True
    )