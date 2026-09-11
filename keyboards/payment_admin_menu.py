from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


PAYMENT_ADMIN_METHODS = [
    ("card", "💳 Bank kartasi"),
    ("click", "📱 Click"),
    ("payme", "💙 Payme"),
    ("uzum", "🟣 Uzum Bank"),
    ("apelsin", "🟡 Apelsin"),
    ("paynet", "🟢 Paynet"),
    ("anor", "🟠 Anor Bank"),
    ("tbc", "🔵 TBC Bank"),
    ("bank", "🏦 Bank o‘tkazmasi"),
    ("other", "🌐 Boshqa"),
]


def payment_admin_keyboard():
    keyboard = []

    for method, name in PAYMENT_ADMIN_METHODS:
        keyboard.append([
            InlineKeyboardButton(
                text=name,
                callback_data=f"admin_payment_{method}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            text="🔙 Orqaga",
            callback_data="admin_settings"
        )
    ])

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )