from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def payment_methods_keyboard(order_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💳 Bank kartasi",
                    callback_data=f"payment_card_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📱 Click",
                    callback_data=f"payment_click_{order_id}"
                ),
                InlineKeyboardButton(
                    text="💙 Payme",
                    callback_data=f"payment_payme_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🟣 Uzum Bank",
                    callback_data=f"payment_uzum_{order_id}"
                ),
                InlineKeyboardButton(
                    text="🟡 Apelsin",
                    callback_data=f"payment_apelsin_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🟢 Paynet",
                    callback_data=f"payment_paynet_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🟠 Anor Bank",
                    callback_data=f"payment_anor_{order_id}"
                ),
                InlineKeyboardButton(
                    text="🔵 TBC Bank",
                    callback_data=f"payment_tbc_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏦 Bank o‘tkazmasi",
                    callback_data=f"payment_bank_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌐 Boshqa",
                    callback_data=f"payment_other_{order_id}"
                )
            ]
        ]
    )