import asyncio
import os
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy import select

from config import BOT_TOKEN, ADMIN_ID, REQUIRED_CHANNELS
from database.db import init_db, async_session, User
from keyboards.main_menu import main_menu

from handlers import payment
from handlers import (
    order,
    books,
    scientific,
    contest,
    design,
    website,
    prices,
    promotions,
    admin
)


dp = Dispatcher()

# =========================================================
# 🌐 RENDER PORT SERVER
# =========================================================

async def render_health_server():
    port = int(os.environ.get("PORT", 10000))

    async def handle_client(reader, writer):
        try:
            await reader.read(1024)

            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain; charset=utf-8\r\n"
                "Content-Length: 2\r\n"
                "Connection: close\r\n"
                "\r\n"
                "OK"
            )

            writer.write(response.encode())
            await writer.drain()

        except Exception:
            pass

        finally:
            writer.close()
            await writer.wait_closed()

    server = await asyncio.start_server(
        handle_client,
        "0.0.0.0",
        port
    )

    print(f"🌐 Render port server ishga tushdi: {port}")

    return server
# =========================================================
# 📢 MAJBURIY OBUNA TUGMALARI
# =========================================================

def subscription_keyboard():
    buttons = []

    for channel in REQUIRED_CHANNELS:
        buttons.append([
            InlineKeyboardButton(
                text=f"➕ {channel['name']}",
                url=channel["url"]
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="✅ Обунани текшириш",
            callback_data="check_subscription"
        )
    ])

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


# =========================================================
# 📢 OBUNANI TEKSHIRISH
# =========================================================

async def check_subscription(
    bot: Bot,
    user_id: int
) -> bool:

    for channel in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(
                chat_id=channel["chat_id"],
                user_id=user_id
            )

            if member.status in ["left", "kicked"]:
                return False

        except TelegramBadRequest:
            return False

    return True


# =========================================================
# 🏠 ASOSIY MENU
# =========================================================

async def show_main_menu(message: Message):

    await message.answer(
        "Ассалому алайкум! 🌷\n\n"
        "<b>ORZU AKADEMIYA</b> расмий ботига хуш келибсиз! ✨\n\n"
        "Биз сизга илмий, ижодий, нашриёт ва медиа "
        "хизматларида профессионал ёрдам берамиз.\n\n"
        "Керакли бўлимни танланг 👇",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


# =========================================================
# 👤 FOYDALANUVCHINI BAZAGA SAQLASH
# =========================================================

async def save_user(message: Message):

    async with async_session() as session:

        result = await session.execute(
            select(User).where(
                User.telegram_id == message.from_user.id
            )
        )

        user = result.scalar_one_or_none()

        if user:

            user.last_seen = datetime.now()
            user.username = message.from_user.username
            user.first_name = message.from_user.first_name
            user.last_name = message.from_user.last_name

        else:

            user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                created_at=datetime.now(),
                last_seen=datetime.now()
            )

            session.add(user)

        await session.commit()


# =========================================================
# 🚀 /START
# =========================================================

@dp.message(CommandStart())
async def start_handler(message: Message):

    # Foydalanuvchini bazaga yozish
    await save_user(message)

    # Majburiy obunani tekshirish
    is_subscribed = await check_subscription(
        message.bot,
        message.from_user.id
    )

    if not is_subscribed:

        await message.answer(
            "📢 <b>Ботдан фойдаланиш учун "
            "каналимизга обуна бўлинг!</b>\n\n"
            "Каналга обуна бўлиб, кейин "
            "<b>Обунани текшириш</b> тугмасини босинг 👇",
            reply_markup=subscription_keyboard(),
            parse_mode="HTML"
        )

        return

    await show_main_menu(message)


# =========================================================
# ✅ OBUNANI QAYTA TEKSHIRISH
# =========================================================

@dp.callback_query(
    lambda c: c.data == "check_subscription"
)
async def subscription_check(
    callback: CallbackQuery
):

    # Foydalanuvchini yangilash
    async with async_session() as session:

        result = await session.execute(
            select(User).where(
                User.telegram_id == callback.from_user.id
            )
        )

        user = result.scalar_one_or_none()

        if user:

            user.last_seen = datetime.now()
            user.username = callback.from_user.username
            user.first_name = callback.from_user.first_name
            user.last_name = callback.from_user.last_name

            await session.commit()

    # Obunani tekshirish
    is_subscribed = await check_subscription(
        callback.bot,
        callback.from_user.id
    )

    if is_subscribed:

        await callback.message.delete()

        await show_main_menu(
            callback.message
        )

        await callback.answer(
            "✅ Обуна тасдиқланди!"
        )

    else:

        await callback.answer(
            "❌ Ҳали каналга обуна бўлмагансиз!",
            show_alert=True
        )


# =========================================================
# 🚀 BOTNI ISHGA TUSHIRISH
# =========================================================

async def main():

    bot = Bot(
        token=BOT_TOKEN
    )

    # Database
    await init_db()

    # Routers
    dp.include_router(admin.router)
    dp.include_router(payment.router)
    dp.include_router(order.router)
    dp.include_router(books.router)
    dp.include_router(scientific.router)
    dp.include_router(contest.router)
    dp.include_router(design.router)
    dp.include_router(website.router)
    dp.include_router(prices.router)
    dp.include_router(promotions.router)
    # Konsol
    print(
        "🚀 ORZU AKADEMIYA bot ishga tushmoqda..."
    )

    print(
        f"👤 Admin ID: {ADMIN_ID}"
    )

    print(
        "📢 Majburiy obuna tizimi: YOQILDI"
    )

    print(
        "🏠 Asosiy menyu: YOQILDI"
    )

    print(
        "📚 Kitob va nashriyot: YOQILDI"
    )

    print(
        "🎓 Ilmiy xizmatlar: YOQILDI"
    )

    print(
        "🏆 Tanlov va loyihalar: YOQILDI"
    )

    print(
        "🎨 Dizayn va media: YOQILDI"
    )

    print(
        "🌐 Sayt yaratish: YOQILDI"
    )

    print(
        "💰 Narxlar: YOQILDI"
    )

    print(
        "🔥 Aksiyalar: YOQILDI"
    )

        # Render PORT server
    server = await render_health_server()

    # Polling
    await dp.start_polling(bot)

    server.close()
    await server.wait_closed()


# =========================================================
# ▶️ START
# =========================================================

if __name__ == "__main__":
    asyncio.run(main())