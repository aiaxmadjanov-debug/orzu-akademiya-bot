import os
from datetime import datetime

from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_URL = f"sqlite+aiosqlite:///{os.path.join(BASE_DIR, 'orzu_akademiya.db')}"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    telegram_id: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        index=True
    )

    username: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    first_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    last_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    last_seen: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    order_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        index=True
    )

    username: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    name: Mapped[str] = mapped_column(
        String(150)
    )

    phone: Mapped[str] = mapped_column(
        String(50)
    )

    service: Mapped[str] = mapped_column(
        String(150)
    )

    task: Mapped[str] = mapped_column(
        Text
    )

    volume: Mapped[str] = mapped_column(
        String(100)
    )

    deadline: Mapped[str] = mapped_column(
        String(100)
    )

    file_id: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    file_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    file_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="new"
    )

    # =========================
    # 💳 TO'LOV TIZIMI
    # =========================

    price: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    payment_status: Mapped[str] = mapped_column(
        String(50),
        default="not_required"
    )

    payment_method: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    receipt_file_id: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    receipt_file_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    receipt_file_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    fake_receipt_warnings: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    payment_checked_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

class PaymentSetting(Base):
    __tablename__ = "payment_settings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    method: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    details: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    service_name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        index=True
    )

    price: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )


engine = create_async_engine(
    DATABASE_URL,
    echo=False
)


async_session = async_sessionmaker(
    engine,
    expire_on_commit=False
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("🗄️ Database: YOQILDI")