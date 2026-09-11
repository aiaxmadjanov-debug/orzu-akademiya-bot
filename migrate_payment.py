import asyncio

from sqlalchemy import text

from database.db import engine


async def migrate():
    columns = {
        "price": "VARCHAR(100)",
        "payment_status": "VARCHAR(50) NOT NULL DEFAULT 'not_required'",
        "payment_method": "VARCHAR(50)",
        "receipt_file_id": "VARCHAR(500)",
        "receipt_file_type": "VARCHAR(50)",
        "receipt_file_name": "VARCHAR(255)",
        "fake_receipt_warnings": "INTEGER NOT NULL DEFAULT 0",
        "payment_checked_at": "DATETIME",
    }

    async with engine.begin() as conn:
        result = await conn.execute(
            text("PRAGMA table_info(orders)")
        )

        existing_columns = {
            row[1] for row in result.fetchall()
        }

        for column_name, column_type in columns.items():
            if column_name not in existing_columns:
                await conn.execute(
                    text(
                        f"ALTER TABLE orders "
                        f"ADD COLUMN {column_name} {column_type}"
                    )
                )
                print(f"✅ Qo‘shildi: {column_name}")
            else:
                print(f"ℹ️ Mavjud: {column_name}")

    print("\n🎉 Database migration muvaffaqiyatli tugadi!")


if __name__ == "__main__":
    asyncio.run(migrate())