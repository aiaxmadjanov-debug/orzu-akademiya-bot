from datetime import datetime

from aiogram import Router, F
from sqlalchemy import select
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database.db import async_session, Order, PaymentSetting
from config import ADMIN_ID


router = Router()


PAYMENT_METHODS = {
    "card": "💳 Bank kartasi",
    "click": "📱 Click",
    "payme": "💙 Payme",
    "uzum": "🟣 Uzum Bank",
    "apelsin": "🟡 Apelsin",
    "paynet": "🟢 Paynet",
    "anor": "🟠 Anor Bank",
    "tbc": "🔵 TBC Bank",
    "bank": "🏦 Bank o‘tkazmasi",
    "other": "🌐 Boshqa",
}


# =========================================================
# 💳 MIJOZ TO‘LOV USULINI TANLAYDI
# =========================================================

@router.callback_query(F.data.startswith("payment_"))
async def select_payment_method(callback: CallbackQuery):

    parts = callback.data.split("_")

    if len(parts) != 3:
        await callback.answer(
            "❌ To‘lov ma’lumotlari noto‘g‘ri.",
            show_alert=True
        )
        return

    method = parts[1]

    try:
        order_id = int(parts[2])
    except ValueError:
        await callback.answer(
            "❌ Buyurtma raqami noto‘g‘ri.",
            show_alert=True
        )
        return

    method_name = PAYMENT_METHODS.get(
        method,
        "🌐 Boshqa"
    )

    async with async_session() as session:

        order = await session.get(
            Order,
            order_id
        )

        if not order:
            await callback.answer(
                "❌ Buyurtma topilmadi.",
                show_alert=True
            )
            return

        if order.user_id != callback.from_user.id:
            await callback.answer(
                "❌ Bu buyurtma sizga tegishli emas.",
                show_alert=True
            )
            return

        result = await session.execute(
            select(PaymentSetting).where(
                PaymentSetting.method == method,
                PaymentSetting.is_active == True
            )
        )

        payment_setting = result.scalar_one_or_none()

        order.payment_method = method
        order.payment_status = "waiting_receipt"

        await session.commit()

        price = order.price
        order_number = order.order_number

        if payment_setting and payment_setting.details:
            details = payment_setting.details
        else:
            details = (
                "⚠️ Ushbu to‘lov usuli uchun "
                "rekvizitlar hali sozlanmagan."
            )

    try:
        await callback.message.edit_reply_markup(
            reply_markup=None
        )
    except Exception:
        pass

    await callback.message.answer(
        "💳 <b>TO‘LOV USULI TANLANDI</b>\n\n"
        f"🆔 <b>Buyurtma:</b> #{order_number}\n"
        f"💰 <b>To‘lov summasi:</b> "
        f"{price or 'Aniqlanmagan'}\n"
        f"💳 <b>Usul:</b> {method_name}\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📌 <b>TO‘LOV REKVIZITLARI</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"{details}\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "💡 To‘lovni amalga oshirgandan so‘ng "
        "chek yoki to‘lov skrinshotini shu yerga yuboring.\n\n"
        "⚠️ Faqat haqiqiy to‘lov chekini yuboring.",
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# 🧾 TO‘LOV CHEKINI QABUL QILISH
# VA ADMINGA YUBORISH
# =========================================================

@router.message(F.photo | F.document)
async def receive_payment_receipt(message: Message):

    user_id = message.from_user.id

    async with async_session() as session:

        result = await session.execute(
            select(Order)
            .where(
                Order.user_id == user_id,
                Order.payment_status == "waiting_receipt"
            )
            .order_by(Order.id.desc())
        )

        order = result.scalars().first()

        if not order:
            await message.answer(
                "❌ <b>Kutilayotgan to‘lov topilmadi.</b>\n\n"
                "Avval buyurtmangiz uchun to‘lov usulini tanlang.",
                parse_mode="HTML"
            )
            return

        if message.photo:

            file_id = message.photo[-1].file_id
            file_type = "photo"
            file_name = "payment_receipt.jpg"

        elif message.document:

            file_id = message.document.file_id
            file_type = "document"
            file_name = (
                message.document.file_name
                or "payment_receipt"
            )

        else:
            return

        order.receipt_file_id = file_id
        order.receipt_file_type = file_type
        order.receipt_file_name = file_name
        order.payment_status = "checking"

        await session.commit()

        order_id = order.id
        order_number = order.order_number
        price = order.price
        payment_method = order.payment_method

    # =====================================================
    # 👤 MIJOZGA
    # =====================================================

    await message.answer(
        "✅ <b>CHEK QABUL QILINDI!</b>\n\n"
        f"🆔 <b>Buyurtma:</b> #{order_number}\n"
        f"💰 <b>Summa:</b> "
        f"{price or 'Aniqlanmagan'}\n"
        f"💳 <b>To‘lov usuli:</b> "
        f"{payment_method or 'Aniqlanmagan'}\n\n"
        "🔍 <b>Holat:</b> To‘lov tekshirilmoqda.\n\n"
        "📌 Admin to‘lovni tekshirganidan "
        "so‘ng sizga natija yuboriladi.",
        parse_mode="HTML"
    )

    # =====================================================
    # 🎛️ ADMIN TUGMALARI
    # =====================================================

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ To‘lovni tasdiqlash",
                    callback_data=(
                        f"confirm_payment_{order_id}"
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ To‘lovni rad etish",
                    callback_data=(
                        f"reject_payment_{order_id}"
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text="⚠️ Shubhali chek",
                    callback_data=(
                        f"fake_payment_{order_id}"
                    )
                )
            ]
        ]
    )

    # =====================================================
    # 👨‍💼 ADMINGA
    # =====================================================

    admin_text = (
        "🧾 <b>YANGI TO‘LOV CHEKI!</b>\n\n"
        f"🆔 <b>Buyurtma:</b> #{order_number}\n"
        f"👤 <b>Mijoz ID:</b> "
        f"<code>{user_id}</code>\n"
        f"💰 <b>Summa:</b> "
        f"{price or 'Aniqlanmagan'}\n"
        f"💳 <b>To‘lov usuli:</b> "
        f"{payment_method or 'Aniqlanmagan'}\n\n"
        "🔍 <b>Holat:</b> To‘lov tekshirilmoqda.\n\n"
        "Quyidagi amalni tanlang 👇"
    )

    if file_type == "photo":

        await message.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=file_id,
            caption=admin_text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    else:

        await message.bot.send_document(
            chat_id=ADMIN_ID,
            document=file_id,
            caption=admin_text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )


# =========================================================
# ✅ TO‘LOVNI TASDIQLASH
# =========================================================

@router.callback_query(
    F.data.startswith("confirm_payment_")
)
async def confirm_payment(callback: CallbackQuery):

    if callback.from_user.id != ADMIN_ID:
        await callback.answer(
            "⛔️ Sizda bu amalni bajarish huquqi yo‘q.",
            show_alert=True
        )
        return

    try:
        order_id = int(
            callback.data.split("_")[-1]
        )
    except ValueError:
        await callback.answer(
            "❌ Buyurtma raqami noto‘g‘ri.",
            show_alert=True
        )
        return

    async with async_session() as session:

        order = await session.get(
            Order,
            order_id
        )

        if not order:
            await callback.answer(
                "❌ Buyurtma topilmadi.",
                show_alert=True
            )
            return

        order.payment_status = "paid"
        order.status = "processing"
        order.payment_checked_at = datetime.now()

        user_id = order.user_id
        order_number = order.order_number
        price = order.price

        await session.commit()

    try:
        await callback.message.edit_reply_markup(
            reply_markup=None
        )
    except Exception:
        pass

    await callback.message.answer(
        "✅ <b>TO‘LOV TASDIQLANDI</b>\n\n"
        f"🆔 <b>Buyurtma:</b> #{order_number}\n"
        f"💰 <b>Summa:</b> "
        f"{price or 'Aniqlanmagan'}\n\n"
        "⚙️ <b>Buyurtma holati:</b> Jarayonda",
        parse_mode="HTML"
    )

    try:
        await callback.bot.send_message(
            user_id,
            "✅ <b>TO‘LOVINGIZ TASDIQLANDI!</b>\n\n"
            f"🆔 <b>Buyurtma:</b> #{order_number}\n"
            f"💰 <b>To‘langan summa:</b> "
            f"{price or 'Aniqlanmagan'}\n\n"
            "⚙️ <b>Buyurtma holati:</b> Jarayonda\n\n"
            "Mutaxassislarimiz buyurtmangiz "
            "ustida ishlashni boshlaydi.",
            parse_mode="HTML"
        )
    except Exception as error:
        print(
            "⚠️ Mijozga tasdiq xabari yuborilmadi:",
            error
        )

    await callback.answer(
        "✅ To‘lov tasdiqlandi."
    )


# =========================================================
# ❌ TO‘LOVNI RAD ETISH
# =========================================================

@router.callback_query(
    F.data.startswith("reject_payment_")
)
async def reject_payment(callback: CallbackQuery):

    if callback.from_user.id != ADMIN_ID:
        await callback.answer(
            "⛔️ Sizda bu amalni bajarish huquqi yo‘q.",
            show_alert=True
        )
        return

    try:
        order_id = int(
            callback.data.split("_")[-1]
        )
    except ValueError:
        await callback.answer(
            "❌ Buyurtma raqami noto‘g‘ri.",
            show_alert=True
        )
        return

    async with async_session() as session:

        order = await session.get(
            Order,
            order_id
        )

        if not order:
            await callback.answer(
                "❌ Buyurtma topilmadi.",
                show_alert=True
            )
            return

        order.payment_status = "rejected"

        user_id = order.user_id
        order_number = order.order_number

        await session.commit()

    try:
        await callback.message.edit_reply_markup(
            reply_markup=None
        )
    except Exception:
        pass

    await callback.message.answer(
        "❌ <b>TO‘LOV RAD ETILDI</b>\n\n"
        f"🆔 <b>Buyurtma:</b> #{order_number}\n\n"
        "Mijozga qayta chek yuborish "
        "haqida xabar yuborildi.",
        parse_mode="HTML"
    )

    try:
        await callback.bot.send_message(
            user_id,
            "❌ <b>TO‘LOV CHEKINGIZ RAD ETILDI</b>\n\n"
            f"🆔 <b>Buyurtma:</b> #{order_number}\n\n"
            "Iltimos, to‘lovni tekshiring va "
            "haqiqiy chekni qayta yuboring.",
            parse_mode="HTML"
        )
    except Exception as error:
        print(
            "⚠️ Mijozga rad etish xabari yuborilmadi:",
            error
        )

    await callback.answer(
        "❌ To‘lov rad etildi."
    )


# =========================================================
# ⚠️ SHUBHALI CHEK
# =========================================================

@router.callback_query(
    F.data.startswith("fake_payment_")
)
async def fake_payment(callback: CallbackQuery):

    if callback.from_user.id != ADMIN_ID:
        await callback.answer(
            "⛔️ Sizda bu amalni bajarish huquqi yo‘q.",
            show_alert=True
        )
        return

    try:
        order_id = int(
            callback.data.split("_")[-1]
        )
    except ValueError:
        await callback.answer(
            "❌ Buyurtma raqami noto‘g‘ri.",
            show_alert=True
        )
        return

    async with async_session() as session:

        order = await session.get(
            Order,
            order_id
        )

        if not order:
            await callback.answer(
                "❌ Buyurtma topilmadi.",
                show_alert=True
            )
            return

        order.payment_status = "suspicious"

        current_warnings = (
            order.fake_receipt_warnings or 0
        )

        order.fake_receipt_warnings = (
            current_warnings + 1
        )

        user_id = order.user_id
        order_number = order.order_number
        warnings = order.fake_receipt_warnings

        await session.commit()

    try:
        await callback.message.edit_reply_markup(
            reply_markup=None
        )
    except Exception:
        pass

    await callback.message.answer(
        "⚠️ <b>SHUBHALI CHEK BELGILANDI</b>\n\n"
        f"🆔 <b>Buyurtma:</b> #{order_number}\n"
        f"⚠️ <b>Ogohlantirishlar:</b> {warnings}",
        parse_mode="HTML"
    )

    try:
        await callback.bot.send_message(
            user_id,
            "⚠️ <b>TO‘LOV CHEKINGIZ QO‘SHIMCHA "
            "TEKSHIRUVGA YUBORILDI</b>\n\n"
            f"🆔 <b>Buyurtma:</b> #{order_number}\n\n"
            "Admin to‘lov ma’lumotlarini qo‘shimcha "
            "tekshirmoqda. Natija sizga yuboriladi.",
            parse_mode="HTML"
        )
    except Exception as error:
        print(
            "⚠️ Mijozga shubhali chek xabari "
            "yuborilmadi:",
            error
        )

    await callback.answer(
        "⚠️ Chek shubhali deb belgilandi."
    )