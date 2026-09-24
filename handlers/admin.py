from sqlalchemy import select

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID, ADMIN_IDS
from database.db import (
    async_session,
    Order,
    User,
    Price,
    PaymentSetting
)
from keyboards.admin_menu import admin_menu
from keyboards.payment_admin_menu import payment_admin_keyboard
from states.admin_states import (
    PriceStates,
    PaymentStates,
    PaymentSettingStates
)
from datetime import datetime
from keyboards.payment_menu import payment_methods_keyboard

router = Router()


# =========================================================
# 👑 ADMIN PANEL
# =========================================================

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer(
            "⛔️ Сизда админ панелга кириш ҳуқуқи йўқ."
        )
        return

    await message.answer(
        "👑 <b>ORZU AKADEMIYA — ADMIN PANEL</b>\n\n"
        "Керакли бўлимни танланг 👇",
        reply_markup=admin_menu(),
        parse_mode="HTML"
    )


# =========================================================
# 📝 BUYURTMALAR STATUS MENYUSI
# =========================================================

def orders_status_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🆕 Янги буюртмалар",
                    callback_data="admin_orders_new"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Жараёнда",
                    callback_data="admin_orders_processing"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💳 Тўлов кутилмоқда",
                    callback_data="admin_orders_payment"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Тугалланган",
                    callback_data="admin_orders_completed"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Бекор қилинган",
                    callback_data="admin_orders_cancelled"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 Барча буюртмалар",
                    callback_data="admin_orders_all"
                )
            ]
        ]
    )


@router.message(lambda message: message.text == "📝 Буюртмалар")
async def admin_orders_menu(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    await message.answer(
        "📝 <b>БУЮРТМАЛАР БОШҚАРУВИ</b>\n\n"
        "Керакли буюртмалар бўлимини танланг 👇",
        reply_markup=orders_status_menu(),
        parse_mode="HTML"
    )


# =========================================================
# 🆕 YANGI BUYURTMALAR
# =========================================================

@router.callback_query(
    lambda callback: callback.data == "admin_orders_new"
)
async def show_new_orders(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer(
            "⛔️ Сизда бу амални бажариш ҳуқуқи йўқ.",
            show_alert=True
        )
        return

    async with async_session() as session:
        result = await session.execute(
            select(Order)
            .where(Order.status == "new")
            .order_by(Order.created_at.desc())
        )

        orders = result.scalars().all()

    if not orders:
        await callback.message.edit_text(
            "🆕 <b>ЯНГИ БУЮРТМАЛАР</b>\n\n"
            "Ҳозирча янги буюртмалар мавжуд эмас.",
            parse_mode="HTML"
        )
        await callback.answer()
        return

    # -----------------------------------------------------
    # 🔘 HAR BIR BUYURTMA UCHUN ALOHIDA TUGMA
    # -----------------------------------------------------

    buttons = []

    for order in orders:
        buttons.append([
            InlineKeyboardButton(
                text=(
                    f"🆕 {order.order_number} — "
                    f"{order.name}"
                ),
                callback_data=f"admin_order_{order.id}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="🔙 Орқага",
            callback_data="admin_orders_back"
        )
    ])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    await callback.message.edit_text(
        "🆕 <b>ЯНГИ БУЮРТМАЛАР</b>\n\n"
        f"Жами: <b>{len(orders)}</b> та\n\n"
        "Керакли буюртмани танланг 👇",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# 📋 BUYURTMA TO‘LIQ MA'LUMOTI
# =========================================================

@router.callback_query(
    lambda callback: callback.data.startswith("admin_order_")
)
async def show_order_details(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer(
            "⛔️ Сизда бу амални бажариш ҳуқуқи йўқ.",
            show_alert=True
        )
        return

    try:
        order_id = int(
            callback.data.replace(
                "admin_order_",
                ""
            )
        )
    except ValueError:
        await callback.answer(
            "❌ Буюртма рақами нотўғри.",
            show_alert=True
        )
        return

    async with async_session() as session:
        result = await session.execute(
            select(Order).where(
                Order.id == order_id
            )
        )

        order = result.scalar_one_or_none()

    if not order:
        await callback.answer(
            "❌ Буюртма топилмади.",
            show_alert=True
        )
        return

    status_names = {
        "new": "🆕 Янги",
        "processing": "🔄 Жараёнда",
        "payment": "💳 Тўлов кутилмоқда",
        "completed": "✅ Тугалланган",
        "cancelled": "❌ Бекор қилинган"
    }

    status_text = status_names.get(
        order.status,
        order.status
    )

    username = (
        f"@{order.username}"
        if order.username
        else "Мавжуд эмас"
    )

    file_text = (
        order.file_name
        if order.file_name
        else "Файл бириктирилмаган"
    )

    text = (
        "📋 <b>БУЮРТМА ТЎЛИҚ МАЪЛУМОТИ</b>\n\n"
        f"🆔 <b>Буюртма рақами:</b>\n"
        f"{order.order_number}\n\n"
        f"👤 <b>Мижоз:</b>\n"
        f"{order.name}\n\n"
        f"📞 <b>Телефон:</b>\n"
        f"{order.phone}\n\n"
        f"💬 <b>Telegram:</b>\n"
        f"{username}\n\n"
        f"🆔 <b>User ID:</b>\n"
        f"{order.user_id}\n\n"
        f"📚 <b>Хизмат:</b>\n"
        f"{order.service}\n\n"
        f"📝 <b>Мавзу / вазифа:</b>\n"
        f"{order.task}\n\n"
        f"📑 <b>Иш ҳажми:</b>\n"
        f"{order.volume}\n\n"
        f"⏰ <b>Муддат:</b>\n"
        f"{order.deadline}\n\n"
        f"📎 <b>Файл:</b>\n"
        f"{file_text}\n\n"
        f"🔄 <b>Статус:</b>\n"
        f"{status_text}\n\n"
        f"📅 <b>Буюртма санаси:</b>\n"
        f"{order.created_at.strftime('%d.%m.%Y %H:%M')}"
    )

    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔄 Статусни ўзгартириш",
                callback_data=f"admin_status_{order.id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="💰 Нарх белгилаш",
                callback_data=f"set_price_{order.id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Буюртмаларга қайтиш",
                callback_data="admin_orders_new"
            )
        ]
    ]
)

    await callback.message.edit_text(
        text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# 🔙 BUYURTMALAR MENYUSIGA QAYTISH
# =========================================================

@router.callback_query(
    lambda callback: callback.data == "admin_orders_back"
)
async def admin_orders_back(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        return

    await callback.message.edit_text(
        "📝 <b>БУЮРТМАЛАР БОШҚАРУВИ</b>\n\n"
        "Керакли бўлимни танланг 👇",
        reply_markup=orders_status_menu(),
        parse_mode="HTML"
    )

    await callback.answer()
# =========================================================
# 🔄 STATUS O‘ZGARTIRISH MENYUSI
# =========================================================

def order_status_menu(order_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🆕 Янги",
                    callback_data=f"set_status_new_{order_id}"
                ),
                InlineKeyboardButton(
                    text="🔄 Жараёнда",
                    callback_data=f"set_status_processing_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💳 Тўлов кутилмоқда",
                    callback_data=f"set_status_payment_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Тугалланган",
                    callback_data=f"set_status_completed_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Бекор қилинган",
                    callback_data=f"set_status_cancelled_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Буюртмага қайтиш",
                    callback_data=f"admin_order_{order_id}"
                )
            ]
        ]
    )


# =========================================================
# 🔄 STATUS O‘ZGARTIRISH
# =========================================================

@router.callback_query(
    lambda callback: callback.data.startswith("admin_status_")
)
async def change_order_status_menu(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer(
            "⛔️ Сизда бу амални бажариш ҳуқуқи йўқ.",
            show_alert=True
        )
        return

    try:
        order_id = int(
            callback.data.replace(
                "admin_status_",
                ""
            )
        )
    except ValueError:
        await callback.answer(
            "❌ Буюртма ID нотўғри.",
            show_alert=True
        )
        return

    async with async_session() as session:
        result = await session.execute(
            select(Order).where(
                Order.id == order_id
            )
        )

        order = result.scalar_one_or_none()

    if not order:
        await callback.answer(
            "❌ Буюртма топилмади.",
            show_alert=True
        )
        return

    await callback.message.edit_text(
        "🔄 <b>БУЮРТМА СТАТУСИНИ ЎЗГАРТИРИШ</b>\n\n"
        f"🆔 <b>{order.order_number}</b>\n"
        f"👤 {order.name}\n\n"
        "Янги статусни танланг 👇",
        reply_markup=order_status_menu(order.id),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# 💾 STATUSNI BAZAGA SAQLASH + MIJOZGA XABAR
# =========================================================

@router.callback_query(
    lambda callback: callback.data.startswith("set_status_")
)
async def set_order_status(callback: CallbackQuery):

    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer(
            "⛔️ Сизда бу амални бажариш ҳуқуқи йўқ.",
            show_alert=True
        )
        return

    parts = callback.data.split("_")

    if len(parts) != 4:
        await callback.answer(
            "❌ Статус маълумоти нотўғри.",
            show_alert=True
        )
        return

    status = parts[2]

    try:
        order_id = int(parts[3])
    except ValueError:
        await callback.answer(
            "❌ Буюртма ID нотўғри.",
            show_alert=True
        )
        return

    allowed_statuses = {
        "new": "🆕 Янги",
        "processing": "🔄 Жараёнда",
        "payment": "💳 Тўлов кутилмоқда",
        "completed": "✅ Тугалланган",
        "cancelled": "❌ Бекор қилинган"
    }

    if status not in allowed_statuses:
        await callback.answer(
            "❌ Номаълум статус.",
            show_alert=True
        )
        return

    async with async_session() as session:

        result = await session.execute(
            select(Order).where(
                Order.id == order_id
            )
        )

        order = result.scalar_one_or_none()

        if not order:
            await callback.answer(
                "❌ Буюртма топилмади.",
                show_alert=True
            )
            return

        order.status = status

        await session.commit()

        order_number = order.order_number
        client_name = order.name
        client_telegram_id = order.user_id
        status_text = allowed_statuses[status]

    # =====================================================
    # 📩 MIJOZGA STATUS O'ZGARGANI HAQIDA XABAR
    # =====================================================

    try:
        await callback.bot.send_message(
            chat_id=client_telegram_id,
            text=(
                "📦 <b>Буюртмангиз статуси янгиланди!</b>\n\n"
                f"🆔 <b>Буюртма:</b> #{order_number}\n"
                f"🔄 <b>Янги статус:</b> {status_text}\n\n"
                "📌 Буюртмангиз бўйича янгиликлар шу ерда "
                "юбориб борилади."
            ),
            parse_mode="HTML"
        )

        client_notified = True

    except Exception:
        client_notified = False

    # =====================================================
    # 👑 ADMIN EKRANI
    # =====================================================

    await callback.message.edit_text(
        "✅ <b>СТАТУС ЯНГИЛАНДИ!</b>\n\n"
        f"🆔 <b>Буюртма:</b> {order_number}\n"
        f"👤 <b>Мижоз:</b> {client_name}\n"
        f"🔄 <b>Янги статус:</b> {status_text}\n\n"
        + (
            "📩 <b>Мижозга хабар юборилди.</b>"
            if client_notified
            else "⚠️ <b>Мижозга хабар юбориб бўлмади.</b>"
        ),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📋 Буюртмани очиш",
                        callback_data=f"admin_order_{order_id}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔙 Янги буюртмалар",
                        callback_data="admin_orders_new"
                    )
                ]
            ]
        ),
        parse_mode="HTML"
    )

    await callback.answer(
        "✅ Статус сақланди!"
    )# =========================================================
# 📋 STATUS BO‘YICHA BUYURTMALARNI KO‘RISH
# =========================================================

async def show_orders_by_status(
    callback: CallbackQuery,
    status: str,
    title: str
):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer(
            "⛔️ Сизда бу амални бажариш ҳуқуқи йўқ.",
            show_alert=True
        )
        return

    async with async_session() as session:
        result = await session.execute(
            select(Order)
            .where(Order.status == status)
            .order_by(Order.created_at.desc())
        )

        orders = result.scalars().all()

    if not orders:
        await callback.message.edit_text(
            f"{title}\n\n"
            "Ҳозирча бу бўлимда буюртмалар мавжуд эмас.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="🔙 Статуслар менюси",
                            callback_data="admin_orders_back"
                        )
                    ]
                ]
            ),
            parse_mode="HTML"
        )
        await callback.answer()
        return

    buttons = []

    for order in orders:
        buttons.append([
            InlineKeyboardButton(
                text=f"{title.split()[0]} {order.order_number} — {order.name}",
                callback_data=f"admin_order_{order.id}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="🔙 Статуслар менюси",
            callback_data="admin_orders_back"
        )
    ])

    await callback.message.edit_text(
        f"{title}\n\n"
        f"Жами: <b>{len(orders)}</b> та\n\n"
        "Керакли буюртмани танланг 👇",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=buttons
        ),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# 🔄 JARAYONDAGI
# =========================================================

@router.callback_query(
    lambda callback: callback.data == "admin_orders_processing"
)
async def show_processing_orders(callback: CallbackQuery):
    await show_orders_by_status(
        callback,
        "processing",
        "🔄 <b>ЖАРАЁНДАГИ БУЮРТМАЛАР</b>"
    )


# =========================================================
# 💳 TO‘LOV KUTILAYOTGAN
# =========================================================

@router.callback_query(
    lambda callback: callback.data == "admin_orders_payment"
)
async def show_payment_orders(callback: CallbackQuery):
    await show_orders_by_status(
        callback,
        "payment",
        "💳 <b>ТЎЛОВ КУТИЛАЁТГАН БУЮРТМАЛАР</b>"
    )


# =========================================================
# ✅ TUGALLANGAN
# =========================================================

@router.callback_query(
    lambda callback: callback.data == "admin_orders_completed"
)
async def show_completed_orders(callback: CallbackQuery):
    await show_orders_by_status(
        callback,
        "completed",
        "✅ <b>ТУГАЛЛАНГАН БУЮРТМАЛАР</b>"
    )


# =========================================================
# ❌ BEKOR QILINGAN
# =========================================================

@router.callback_query(
    lambda callback: callback.data == "admin_orders_cancelled"
)
async def show_cancelled_orders(callback: CallbackQuery):
    await show_orders_by_status(
        callback,
        "cancelled",
        "❌ <b>БЕКОР ҚИЛИНГАН БУЮРТМАЛАР</b>"
    )


# =========================================================
# 📋 BARCHA BUYURTMALAR
# =========================================================

@router.callback_query(
    lambda callback: callback.data == "admin_orders_all"
)
async def show_all_orders(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer(
            "⛔️ Сизда бу амални бажариш ҳуқуқи йўқ.",
            show_alert=True
        )
        return

    async with async_session() as session:
        result = await session.execute(
            select(Order)
            .order_by(Order.created_at.desc())
        )

        orders = result.scalars().all()

    if not orders:
        await callback.message.edit_text(
            "📋 <b>БАРЧА БУЮРТМАЛАР</b>\n\n"
            "Ҳозирча бирорта ҳам буюртма мавжуд эмас.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="🔙 Статуслар менюси",
                            callback_data="admin_orders_back"
                        )
                    ]
                ]
            ),
            parse_mode="HTML"
        )
        await callback.answer()
        return

    status_names = {
        "new": "🆕",
        "processing": "🔄",
        "payment": "💳",
        "completed": "✅",
        "cancelled": "❌"
    }

    buttons = []

    for order in orders:
        status_icon = status_names.get(
            order.status,
            "❓"
        )

        buttons.append([
            InlineKeyboardButton(
                text=(
                    f"{status_icon} "
                    f"{order.order_number} — "
                    f"{order.name}"
                ),
                callback_data=f"admin_order_{order.id}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="🔙 Статуслар менюси",
            callback_data="admin_orders_back"
        )
    ])

    await callback.message.edit_text(
        "📋 <b>БАРЧА БУЮРТМАЛАР</b>\n\n"
        f"Жами: <b>{len(orders)}</b> та\n\n"
        "Керакли буюртмани танланг 👇",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=buttons
        ),
        parse_mode="HTML"
    )

    await callback.answer()
# =========================================================
# 📊 STATISTIKA MENYUSI
# =========================================================

from datetime import datetime, timedelta
from sqlalchemy import func


def statistics_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📅 Бугун",
                    callback_data="admin_stats_today"
                ),
                InlineKeyboardButton(
                    text="📆 Шу ҳафта",
                    callback_data="admin_stats_week"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🗓 Шу ой",
                    callback_data="admin_stats_month"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Админ панел",
                    callback_data="admin_stats_back"
                )
            ]
        ]
    )


# =========================================================
# 📊 STATISTIKA TUGMASI
# =========================================================

@router.message(lambda message: message.text == "📊 Статистика")
async def admin_statistics(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    await message.answer(
        "📊 <b>СТАТИСТИКА</b>\n\n"
        "Қайси давр статистикасини кўришни танланг 👇",
        reply_markup=statistics_menu(),
        parse_mode="HTML"
    )


# =========================================================
# 📈 STATISTIKANI HISOBLASH
# =========================================================

async def get_statistics(start_date: datetime):
    async with async_session() as session:

        # Жами буюртмалар
        total_result = await session.execute(
            select(func.count(Order.id))
            .where(Order.created_at >= start_date)
        )
        total = total_result.scalar() or 0

        # Янги
        new_result = await session.execute(
            select(func.count(Order.id))
            .where(
                Order.created_at >= start_date,
                Order.status == "new"
            )
        )
        new = new_result.scalar() or 0

        # Жараёнда
        processing_result = await session.execute(
            select(func.count(Order.id))
            .where(
                Order.created_at >= start_date,
                Order.status == "processing"
            )
        )
        processing = processing_result.scalar() or 0

        # Тўлов
        payment_result = await session.execute(
            select(func.count(Order.id))
            .where(
                Order.created_at >= start_date,
                Order.status == "payment"
            )
        )
        payment = payment_result.scalar() or 0

        # Тугалланган
        completed_result = await session.execute(
            select(func.count(Order.id))
            .where(
                Order.created_at >= start_date,
                Order.status == "completed"
            )
        )
        completed = completed_result.scalar() or 0

        # Бекор қилинган
        cancelled_result = await session.execute(
            select(func.count(Order.id))
            .where(
                Order.created_at >= start_date,
                Order.status == "cancelled"
            )
        )
        cancelled = cancelled_result.scalar() or 0

    return {
        "total": total,
        "new": new,
        "processing": processing,
        "payment": payment,
        "completed": completed,
        "cancelled": cancelled
    }


# =========================================================
# 📊 STATISTIKA EKRANI
# =========================================================

async def show_statistics(
    callback: CallbackQuery,
    period_name: str,
    start_date: datetime
):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer(
            "⛔️ Сизда бу амални бажариш ҳуқуқи йўқ.",
            show_alert=True
        )
        return

    stats = await get_statistics(start_date)

    text = (
        f"📊 <b>СТАТИСТИКА — {period_name}</b>\n\n"
        f"📝 <b>Жами буюртмалар:</b> "
        f"{stats['total']} та\n\n"
        f"🆕 <b>Янги:</b> "
        f"{stats['new']} та\n"
        f"🔄 <b>Жараёнда:</b> "
        f"{stats['processing']} та\n"
        f"💳 <b>Тўлов кутилмоқда:</b> "
        f"{stats['payment']} та\n"
        f"✅ <b>Тугалланган:</b> "
        f"{stats['completed']} та\n"
        f"❌ <b>Бекор қилинган:</b> "
        f"{stats['cancelled']} та\n\n"
        "📅 <b>Ҳисоблаш вақти:</b> "
        f"{datetime.now().strftime('%d.%m.%Y %H:%M')}"
    )

    await callback.message.edit_text(
        text,
        reply_markup=statistics_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# 📅 BUGUN
# =========================================================

@router.callback_query(
    lambda callback: callback.data == "admin_stats_today"
)
async def statistics_today(callback: CallbackQuery):
    now = datetime.now()

    start_date = datetime(
        now.year,
        now.month,
        now.day
    )

    await show_statistics(
        callback,
        "БУГУН",
        start_date
    )


# =========================================================
# 📆 SHU HAFTA
# =========================================================

@router.callback_query(
    lambda callback: callback.data == "admin_stats_week"
)
async def statistics_week(callback: CallbackQuery):
    now = datetime.now()

    start_date = (
        now - timedelta(
            days=now.weekday()
        )
    ).replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    await show_statistics(
        callback,
        "ШУ ҲАФТА",
        start_date
    )


# =========================================================
# 🗓 SHU OY
# =========================================================

@router.callback_query(
    lambda callback: callback.data == "admin_stats_month"
)
async def statistics_month(callback: CallbackQuery):
    now = datetime.now()

    start_date = datetime(
        now.year,
        now.month,
        1
    )

    await show_statistics(
        callback,
        "ШУ ОЙ",
        start_date
    )


# =========================================================
# 🔙 ADMIN PANELGA QAYTISH
# =========================================================

@router.callback_query(
    lambda callback: callback.data == "admin_stats_back"
)
async def statistics_back(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        return

    await callback.message.delete()

    await callback.message.answer(
        "👑 <b>ORZU AKADEMIYA — ADMIN PANEL</b>\n\n"
        "Керакли бўлимни танланг 👇",
        reply_markup=admin_menu(),
        parse_mode="HTML"
    )

    await callback.answer()
# =========================================================
# 👥 FOYDALANUVCHILAR STATISTIKASI
# =========================================================

@router.message(lambda message: message.text == "👥 Фойдаланувчилар")
async def admin_users(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    now = datetime.now()

    today_start = now.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    week_start = (
        today_start - timedelta(
            days=today_start.weekday()
        )
    )

    month_start = today_start.replace(
        day=1
    )

    async with async_session() as session:

        total_result = await session.execute(
            select(func.count(User.id))
        )
        total = total_result.scalar() or 0

        today_result = await session.execute(
            select(func.count(User.id))
            .where(User.created_at >= today_start)
        )
        today = today_result.scalar() or 0

        week_result = await session.execute(
            select(func.count(User.id))
            .where(User.created_at >= week_start)
        )
        week = week_result.scalar() or 0

        month_result = await session.execute(
            select(func.count(User.id))
            .where(User.created_at >= month_start)
        )
        month = month_result.scalar() or 0

        active_result = await session.execute(
            select(func.count(User.id))
            .where(User.last_seen >= today_start)
        )
        active_today = active_result.scalar() or 0

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👥 Фойдаланувчилар рўйхати",
                    callback_data="admin_users_list"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Админ панел",
                    callback_data="admin_users_back"
                )
            ]
        ]
    )

    await message.answer(
        "👥 <b>ФОЙДАЛАНУВЧИЛАР СТАТИСТИКАСИ</b>\n\n"
        f"👥 <b>Жами:</b> {total} та\n\n"
        f"🆕 <b>Бугун қўшилган:</b> {today} та\n"
        f"📆 <b>Шу ҳафта қўшилган:</b> {week} та\n"
        f"🗓 <b>Шу ой қўшилган:</b> {month} та\n\n"
        f"🟢 <b>Бугун фаол:</b> {active_today} та\n\n"
        f"🕐 <b>Янгиланган:</b> "
        f"{now.strftime('%d.%m.%Y %H:%M')}",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
# =========================================================
# 👥 FOYDALANUVCHILAR RO‘YXATI
# =========================================================

@router.callback_query(
    lambda callback: callback.data == "admin_users_list"
)
async def admin_users_list(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer(
            "⛔️ Сизда бу амални бажариш ҳуқуқи йўқ.",
            show_alert=True
        )
        return

    async with async_session() as session:
        result = await session.execute(
            select(User)
            .order_by(User.last_seen.desc())
        )

        users = result.scalars().all()

    if not users:
        await callback.message.edit_text(
            "👥 <b>ФОЙДАЛАНУВЧИЛАР</b>\n\n"
            "Ҳозирча фойдаланувчилар мавжуд эмас.",
            parse_mode="HTML"
        )
        await callback.answer()
        return

    buttons = []

    for user in users:
        username = (
            f"@{user.username}"
            if user.username
            else user.first_name or "Номаълум"
        )

        buttons.append([
            InlineKeyboardButton(
                text=f"👤 {username}",
                callback_data=f"admin_user_{user.id}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="🔙 Орқага",
            callback_data="admin_users_back"
        )
    ])

    await callback.message.edit_text(
        "👥 <b>ФОЙДАЛАНУВЧИЛАР РЎЙХАТИ</b>\n\n"
        f"Жами: <b>{len(users)}</b> та\n\n"
        "Керакли фойдаланувчини танланг 👇",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=buttons
        ),
        parse_mode="HTML"
    )

    await callback.answer()
# =========================================================
# 👤 FOYDALANUVCHI MA'LUMOTLARI
# =========================================================

@router.callback_query(
    lambda callback: callback.data.startswith("admin_user_")
)
async def admin_user_detail(callback: CallbackQuery):

    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer(
            "⛔️ Сизда бу амални бажариш ҳуқуқи йўқ.",
            show_alert=True
        )
        return

    user_id = int(
        callback.data.replace("admin_user_", "")
    )

    async with async_session() as session:

        # Foydalanuvchini olish
        user_result = await session.execute(
            select(User).where(
                User.id == user_id
            )
        )

        user = user_result.scalar_one_or_none()

        if not user:
            await callback.answer(
                "❌ Фойдаланувчи топилмади.",
                show_alert=True
            )
            return

        # Shu foydalanuvchining buyurtmalari
        orders_result = await session.execute(
            select(func.count(Order.id))
            .where(Order.user_id == user.telegram_id)
        )

        orders_count = orders_result.scalar() or 0

    username = (
        f"@{user.username}"
        if user.username
        else "Йўқ"
    )

    full_name = " ".join(
        part for part in [
            user.first_name,
            user.last_name
        ]
        if part
    ) or "Номаълум"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Фойдаланувчилар рўйхати",
                    callback_data="admin_users_list"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 Админ панел",
                    callback_data="admin_users_back"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        "👤 <b>ФОЙДАЛАНУВЧИ МАЪЛУМОТЛАРИ</b>\n\n"
        f"👤 <b>Исм:</b> {full_name}\n"
        f"🔹 <b>Username:</b> {username}\n"
        f"🆔 <b>Telegram ID:</b> <code>{user.telegram_id}</code>\n\n"
        f"📅 <b>Ботга қўшилган:</b> "
        f"{user.created_at.strftime('%d.%m.%Y %H:%M')}\n"
        f"🕐 <b>Охирги фаоллик:</b> "
        f"{user.last_seen.strftime('%d.%m.%Y %H:%M')}\n\n"
        f"📦 <b>Буюртмалар сони:</b> {orders_count} та",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    await callback.answer()
# =========================================================
# 🔙 FOYDALANUVCHILAR MENYUSIDAN ORQAGA
# =========================================================

@router.callback_query(
    lambda callback: callback.data == "admin_users_back"
)
async def admin_users_back(callback: CallbackQuery):

    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer(
            "⛔️ Сизда бу амални бажариш ҳуқуқи йўқ.",
            show_alert=True
        )
        return

    await callback.message.edit_text(
        "⚙️ <b>АДМИН ПАНЕЛЬ</b>\n\n"
        "Керакли бўлимни танланг 👇",
        parse_mode="HTML"
    )

    await callback.answer()
# =========================================================
# 📦 BUYURTMA TAFSILOTLARI
# =========================================================

@router.callback_query(
    lambda callback: callback.data.startswith("admin_order_")
)
async def admin_order_detail(callback: CallbackQuery):

    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer(
            "⛔️ Сизда бу амални бажариш ҳуқуқи йўқ.",
            show_alert=True
        )
        return

    order_id = int(
        callback.data.replace("admin_order_", "")
    )

    async with async_session() as session:

        result = await session.execute(
            select(Order).where(
                Order.id == order_id
            )
        )

        order_item = result.scalar_one_or_none()

    if not order_item:
        await callback.answer(
            "❌ Буюртма топилмади.",
            show_alert=True
        )
        return

    status_names = {
        "new": "🆕 Янги",
        "processing": "🔄 Жараёнда",
        "waiting_payment": "💳 Тўлов кутилмоқда",
        "completed": "✅ Тугалланган",
        "cancelled": "❌ Бекор қилинган"
    }

    status = status_names.get(
        order_item.status,
        order_item.status
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 Статусни ўзгартириш",
                    callback_data=f"admin_order_status_{order_item.id}"
                )
            ],
InlineKeyboardButton(
    text="💰 Нарх белгилаш",
    callback_data=f"set_price_{order.id}"
)

            [
                InlineKeyboardButton(
                    text="🔙 Буюртмалар",
                    callback_data="admin_orders_back"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        "📦 <b>БУЮРТМА ТАФСИЛОТЛАРИ</b>\n\n"
        f"🔢 <b>Буюртма:</b> #{order_item.order_number}\n"
        f"📌 <b>Статус:</b> {status}\n\n"
        f"👤 <b>Исм:</b> {order_item.name}\n"
        f"🔹 <b>Username:</b> "
        f"@{order_item.username if order_item.username else 'Йўқ'}\n"
        f"📞 <b>Телефон:</b> {order_item.phone}\n\n"
        f"🛠 <b>Хизмат:</b> {order_item.service}\n"
        f"📝 <b>Топшириқ:</b>\n{order_item.task}\n\n"
        f"📐 <b>Ҳажм:</b> {order_item.volume}\n"
        f"⏰ <b>Муддат:</b> {order_item.deadline}\n\n"
        f"📎 <b>Файл:</b> "
        f"{order_item.file_name if order_item.file_name else 'Йўқ'}\n\n"
        f"🗓 <b>Буюртма берилган:</b> "
        f"{order_item.created_at.strftime('%d.%m.%Y %H:%M')}",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    await callback.answer()
# =========================================================
# 🔄 BUYURTMA STATUSINI O'ZGARTIRISH
# =========================================================

@router.callback_query(
    lambda callback: callback.data.startswith("admin_order_status_")
)
async def admin_order_status_menu(callback: CallbackQuery):

    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer(
            "⛔️ Сизда бу амални бажариш ҳуқуқи йўқ.",
            show_alert=True
        )
        return

    order_id = int(
        callback.data.replace("admin_order_status_", "")
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🆕 Янги",
                    callback_data=f"set_status_new_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Жараёнда",
                    callback_data=f"set_status_processing_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💳 Тўлов кутилмоқда",
                    callback_data=f"set_status_waiting_payment_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Тугалланган",
                    callback_data=f"set_status_completed_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Бекор қилинган",
                    callback_data=f"set_status_cancelled_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Буюртмага қайтиш",
                    callback_data=f"admin_order_{order_id}"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        "🔄 <b>БУЮРТМА СТАТУСИ</b>\n\n"
        "Янги статусни танланг 👇",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    await callback.answer()
@router.message(F.text == "💰 Нархларни бошқариш")
async def manage_prices(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="➕ Нарх қўшиш"),
                KeyboardButton(text="📋 Нархлар рўйхати")
            ],
            [
                KeyboardButton(text="✏️ Нархни таҳрирлаш"),
                KeyboardButton(text="🔄 Нарх ҳолати")
            ],
            [
                KeyboardButton(text="🗑 Нархни ўчириш")
            ],
            [
                KeyboardButton(text="⬅️ Админ меню")
            ]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "💰 <b>НАРХЛАРНИ БОШҚАРИШ</b>\n\n"
        "Керакли амални танланг 👇",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
@router.message(F.text == "➕ Нарх қўшиш")
async def add_price_start(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return

    await state.set_state(PriceStates.waiting_service_name)

    await message.answer(
        "➕ <b>ЯНГИ НАРХ ҚЎШИШ</b>\n\n"
        "1️⃣ Хизмат номини киритинг:\n\n"
        "Масалан:\n"
        "<i>Илмий мақола ёзиш</i>",
        parse_mode="HTML"
    )


@router.message(PriceStates.waiting_service_name)
async def add_price_service_name(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return

    service_name = message.text.strip()

    if len(service_name) < 2:
        await message.answer(
            "❌ Хизмат номи жуда қисқа.\n\n"
            "Илтимос, қайта киритинг."
        )
        return

    await state.update_data(service_name=service_name)
    await state.set_state(PriceStates.waiting_price)

    await message.answer(
        "💵 Энди хизмат нархини киритинг:\n\n"
        "Масалан:\n"
        "<i>150 000 сўм</i>\n"
        "ёки\n"
        "<i>50$</i>",
        parse_mode="HTML"
    )
@router.message(PriceStates.waiting_price)
async def add_price_value(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return

    price = message.text.strip()

    if len(price) < 1:
        await message.answer(
            "❌ Нарх киритилмади.\n\n"
            "Илтимос, нархни қайта киритинг."
        )
        return

    await state.update_data(price=price)
    await state.set_state(PriceStates.waiting_description)

    await message.answer(
        "📝 Энди хизмат тавсифини киритинг.\n\n"
        "Масалан:\n"
        "<i>7 бетлик илмий мақола тайёрлаш хизмати.</i>\n\n"
        "Агар тавсиф керак бўлмаса, <b>—</b> белгисини юборинг.",
        parse_mode="HTML"
    )
@router.message(PriceStates.waiting_description)
async def add_price_description(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return

    description = message.text.strip()

    if description == "—":
        description = None

    data = await state.get_data()

    service_name = data.get("service_name")
    price = data.get("price")

    now = datetime.now()

    async with async_session() as session:
        new_price = Price(
            service_name=service_name,
            price=price,
            description=description,
            is_active=True,
            created_at=now,
            updated_at=now
        )

        session.add(new_price)
        await session.commit()

    await state.clear()

    await message.answer(
        "✅ <b>НАРХ МУВАФФАҚИЯТЛИ ҚЎШИЛДИ!</b>\n\n"
        f"📌 <b>Хизмат:</b> {service_name}\n"
        f"💵 <b>Нарх:</b> {price}\n"
        f"📝 <b>Тавсиф:</b> {description or 'Кўрсатилмаган'}\n\n"
        "Нарх энди базага сақланди. ✅",
        parse_mode="HTML"
    )
@router.callback_query(F.data.startswith("set_price_"))
async def set_order_price_start(
    callback: CallbackQuery,
    state: FSMContext
):
    if callback.from_user.id not in ADMIN_IDS:
        return

    order_id = int(callback.data.split("_")[-1])

    await state.update_data(order_id=order_id)
    await state.set_state(PaymentStates.waiting_order_price)

    await callback.message.answer(
        "💰 <b>БУЮРТМА НАРХИНИ БЕЛГИЛАШ</b>\n\n"
        "Ушбу буюртма учун нархни киритинг.\n\n"
        "Масалан:\n"
        "💵 <i>250 000 сўм</i>\n"
        "ёки\n"
        "💵 <i>50$</i>",
        parse_mode="HTML"
    )

    await callback.answer()


@router.message(PaymentStates.waiting_order_price)
async def set_order_price_finish(
    message: Message,
    state: FSMContext
):
    if message.from_user.id not in ADMIN_IDS:
        return

    price = (message.text or "").strip()

    if not price:
        await message.answer(
            "❌ Нарх киритилмади.\n\n"
            "Илтимос, нархни қайта киритинг."
        )
        return

    data = await state.get_data()
    order_id = data.get("order_id")

    if not order_id:
        await state.clear()
        await message.answer(
            "❌ Буюртма маълумоти топилмади.\n\n"
            "Илтимос, қайта уриниб кўринг."
        )
        return

    async with async_session() as session:

        order = await session.get(
            Order,
            order_id
        )

        if not order:
            await state.clear()
            await message.answer(
                "❌ Буюртма топилмади."
            )
            return

        order.price = price
        order.payment_status = "waiting_confirmation"

        await session.commit()

        user_id = order.user_id
        order_number = order.order_number
        client_name = order.name

    await state.clear()

    # =====================================================
    # 👑 ADMINDA NARX SAQLANGANI HAQIDA
    # =====================================================

    await message.answer(
        "✅ <b>НАРХ МУВАФФАҚИЯТЛИ БЕЛГИЛАНДИ!</b>\n\n"
        f"🆔 <b>Буюртма:</b> #{order_number}\n"
        f"👤 <b>Мижоз:</b> {client_name}\n"
        f"💰 <b>Нарх:</b> {price}\n\n"
        "📩 Нарх мижозга юборилди.\n"
        "⏳ Мижознинг жавоби кутилмоқда.",
        parse_mode="HTML"
    )

    # =====================================================
    # 👤 MIJOZGA ROZI / RAD ETISH TUGMALARI
    # =====================================================

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Розиман, бошланг",
                    callback_data=f"price_accept_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Рад этаман",
                    callback_data=f"price_reject_{order_id}"
                )
            ]
        ]
    )

    try:

        await message.bot.send_message(
            chat_id=user_id,
            text=(
    "💰 <b>БУЮРТМАНГИЗ НАРХИ ТАЙЁР!</b>\n\n"
    f"🆔 <b>Буюртма:</b> #{order_number}\n"
    f"💵 <b>Белгиланган нарх:</b> {price}\n\n"
    "━━━━━━━━━━━━━━━━━━\n\n"
    "Ушбу нархга розимисиз?\n\n"
    "Агар рози бўлсангиз, "
    "«Розиман, бошланг» тугмасини босинг.\n\n"
    "Агар нарх сизга мос келмаса, "
    "«Рад этаман» тугмасини босинг."
),
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    except Exception as error:

        print(
            "⚠️ Мижозга нарх юборилмади:",
            error
        )
# =========================================================
# ✅ MIJOZ NARXGA ROZI
# =========================================================

@router.callback_query(
    F.data.startswith("price_accept_")
)
async def client_accept_price(
    callback: CallbackQuery
):

    try:
        order_id = int(
            callback.data.replace(
                "price_accept_",
                "",
                1
            )
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

        # Faqat shu buyurtmaning egasi bosishi mumkin
        if order.user_id != callback.from_user.id:
            await callback.answer(
                "⛔️ Bu buyurtma sizga tegishli emas.",
                show_alert=True
            )
            return

        # Faqat narx tasdiqlanishini kutayotgan bo‘lsa
        if order.payment_status != "waiting_confirmation":
            await callback.answer(
                "⚠️ Bu buyurtma bo‘yicha javob allaqachon berilgan.",
                show_alert=True
            )
            return

        order.payment_status = "price_accepted"
        order.status = "processing"

        order_number = order.order_number
        price = order.price
        client_name = order.name
        user_id = order.user_id

        await session.commit()

    # Mijozga tugmalarni olib tashlab tasdiq xabari
    try:
        await callback.message.edit_reply_markup(
            reply_markup=None
        )
    except Exception:
        pass

    await callback.message.answer(
        "✅ <b>НАРХГА РОЗИ БЎЛДИНГИЗ!</b>\n\n"
        f"🆔 <b>Буюртма:</b> #{order_number}\n"
        f"💰 <b>Нарх:</b> {price}\n\n"
        "🚀 Буюртмангиз иш жараёнига қабул қилинди.\n\n"
        "📌 Кейинги босқич бўйича маълумот "
        "сизга шу ерда юборилади.",
        parse_mode="HTML"
    )

        # Barcha adminlarga xabar
    for admin_id in ADMIN_IDS:
        try:
            await callback.bot.send_message(
                chat_id=admin_id,
                text=(
                    "✅ <b>МИЖОЗ НАРХГА РОЗИ БЎЛДИ!</b>\n\n"
                    f"🆔 <b>Буюртма:</b> #{order_number}\n"
                    f"👤 <b>Мижоз:</b> {client_name}\n"
                    f"🆔 <b>User ID:</b> <code>{user_id}</code>\n"
                    f"💰 <b>Нарх:</b> {price}\n\n"
                    "🔄 <b>Статус:</b> Буюртма иш жараёнида."
                ),
                parse_mode="HTML"
            )

        except Exception as error:
            print(
                f"⚠️ Admin {admin_id} ga rozilik xabari yuborilmadi:",
                error
            )

    await callback.answer(
        "✅ Нарх қабул қилинди!"
    )


# =========================================================
# ❌ MIJOZ NARXNI RAD ETDI
# =========================================================

@router.callback_query(
    F.data.startswith("price_reject_")
)
async def client_reject_price(
    callback: CallbackQuery
):

    try:
        order_id = int(
            callback.data.replace(
                "price_reject_",
                "",
                1
            )
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

        # Faqat buyurtma egasi rad eta oladi
        if order.user_id != callback.from_user.id:
            await callback.answer(
                "⛔️ Bu buyurtma sizga tegishli emas.",
                show_alert=True
            )
            return

        if order.payment_status != "waiting_confirmation":
            await callback.answer(
                "⚠️ Bu buyurtma bo‘yicha javob allaqachon berilgan.",
                show_alert=True
            )
            return

        order.payment_status = "price_rejected"
        order.status = "cancelled"

        order_number = order.order_number
        price = order.price
        client_name = order.name
        user_id = order.user_id

        await session.commit()

    # Tugmalarni olib tashlash
    try:
        await callback.message.edit_reply_markup(
            reply_markup=None
        )
    except Exception:
        pass

    await callback.message.answer(
        "❌ <b>НАРХ РАД ЭТИЛДИ</b>\n\n"
        f"🆔 <b>Буюртма:</b> #{order_number}\n"
        f"💰 <b>Нарх:</b> {price}\n\n"
        "Буюртма бекор қилинди.\n\n"
        "Агар бошқа нарх бўйича келишмоқчи бўлсангиз, "
        "админ билан боғланишингиз мумкин.",
        parse_mode="HTML"
    )

        # Barcha adminlarga xabar
    for admin_id in ADMIN_IDS:
        try:
            await callback.bot.send_message(
                chat_id=admin_id,
                text=(
                    "❌ <b>МИЖОЗ НАРХНИ РАД ЭТДИ!</b>\n\n"
                    f"🆔 <b>Буюртма:</b> #{order_number}\n"
                    f"👤 <b>Мижоз:</b> {client_name}\n"
                    f"🆔 <b>User ID:</b> <code>{user_id}</code>\n"
                    f"💰 <b>Таклиф қилинган нарх:</b> {price}\n\n"
                    "❌ <b>Натижа:</b> Мижоз нархга рози бўлмади."
                ),
                parse_mode="HTML"
            )

        except Exception as error:
            print(
                f"⚠️ Admin {admin_id} ga rad etish xabari yuborilmadi:",
                error
            )

    await callback.answer(
        "❌ Нарх рад этилди."
    )
# =========================================================
# ⚙️ ADMIN SOZLAMALARI
# =========================================================

@router.message(F.text == "⚙️ Созламалар")
async def admin_settings(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💳 To‘lov rekvizitlari",
                    callback_data="admin_payment_settings"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Admin panel",
                    callback_data="admin_settings_back"
                )
            ]
        ]
    )

    await message.answer(
        "⚙️ <b>ADMIN SOZLAMALARI</b>\n\n"
        "Kerakli sozlamani tanlang 👇",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
# =========================================================
# 💳 TO‘LOV REKVIZITLARI BOSHQARUVI
# =========================================================

@router.callback_query(
    F.data == "admin_payment_settings"
)
async def admin_payment_settings(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer(
            "⛔️ Сизда бу амални бажариш ҳуқуқи йўқ.",
            show_alert=True
        )
        return

    await callback.message.edit_text(
        "💳 <b>TO‘LOV REKVIZITLARI</b>\n\n"
        "Kerakli to‘lov usulini tanlang 👇\n\n"
        "📌 Shu yer orqali karta raqami, Click, Payme "
        "va boshqa to‘lov rekvizitlarini o‘zgartirishingiz mumkin.",
        reply_markup=payment_admin_keyboard(),
        parse_mode="HTML"
    )

    await callback.answer()
# =========================================================
# 💳 TO‘LOV USULI REKVIZITLARINI SOZLASH
# =========================================================

@router.callback_query(
    F.data.startswith("admin_payment_")
)
async def admin_payment_method_settings(
    callback: CallbackQuery,
    state: FSMContext
):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer(
            "⛔️ Сизда бу амални бажариш ҳуқуқи йўқ.",
            show_alert=True
        )
        return

    method = callback.data.replace(
        "admin_payment_",
        "",
        1
    )

    method_names = {
        "card": "💳 Bank kartasi",
        "click": "📱 Click",
        "payme": "💙 Payme",
        "uzum": "🟣 Uzum Bank",
        "apelsin": "🟡 Apelsin",
        "paynet": "🟢 Paynet",
        "anor": "🟠 Anor Bank",
        "tbc": "🔵 TBC Bank",
        "bank": "🏦 Bank o‘tkazmasi",
        "other": "🌐 Boshqa"
    }

    method_name = method_names.get(
        method,
        "🌐 Boshqa"
    )

    await state.update_data(
        payment_method=method,
        payment_method_name=method_name
    )

    await state.set_state(
        PaymentSettingStates.waiting_method_details
    )

    await callback.message.answer(
        "💳 <b>TO‘LOV REKVIZITLARI</b>\n\n"
        f"📌 <b>Usul:</b> {method_name}\n\n"
        "Endi ushbu to‘lov usuli uchun rekvizitlarni yuboring.\n\n"
        "Masalan:\n"
        "💳 Karta: 8600 1234 5678 9012\n"
        "👤 Ism: Ali Valiyev\n\n"
        "Yoki Click / Payme uchun kerakli telefon "
        "raqami va boshqa ma’lumotlarni yozishingiz mumkin.\n\n"
        "📌 Mijoz to‘lov vaqtida aynan shu ma’lumotlarni ko‘radi.",
        parse_mode="HTML"
    )

    await callback.answer()
# =========================================================
# 💾 TO‘LOV REKVIZITLARINI SAQLASH
# =========================================================

@router.message(
    PaymentSettingStates.waiting_method_details
)
async def save_payment_method_details(
    message: Message,
    state: FSMContext
):
    if message.from_user.id not in ADMIN_IDS:
        return

    details = (message.text or "").strip()

    if not details:
        await message.answer(
            "❌ Rekvizitlar bo‘sh bo‘lishi mumkin emas.\n\n"
            "Iltimos, to‘lov ma’lumotlarini qayta yuboring."
        )
        return

    data = await state.get_data()

    method = data.get("payment_method")
    method_name = data.get("payment_method_name")

    if not method:
        await state.clear()
        await message.answer(
            "❌ To‘lov usuli ma’lumoti topilmadi.\n\n"
            "Iltimos, qaytadan urinib ko‘ring."
        )
        return

    async with async_session() as session:
        result = await session.execute(
            select(PaymentSetting).where(
                PaymentSetting.method == method
            )
        )

        setting = result.scalar_one_or_none()

        now = datetime.now()

        if setting:
            setting.name = method_name
            setting.details = details
            setting.is_active = True
            setting.updated_at = now
        else:
            setting = PaymentSetting(
                method=method,
                name=method_name,
                details=details,
                is_active=True,
                created_at=now,
                updated_at=now
            )
            session.add(setting)

        await session.commit()

    await state.clear()

    await message.answer(
        "✅ <b>REKVIZITLAR SAQLANDI!</b>\n\n"
        f"💳 <b>To‘lov usuli:</b> {method_name}\n\n"
        "📌 Mijoz ushbu to‘lov usulini tanlaganda "
        "saqlangan rekvizitlar unga ko‘rsatiladi.",
        parse_mode="HTML"
    )