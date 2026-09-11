from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):

    # =====================================================
    # 👤 UMUMIY MA'LUMOTLAR
    # =====================================================

    waiting_name = State()
    waiting_phone = State()

    # =====================================================
    # 📚 XIZMAT TANLASH
    # =====================================================

    waiting_service = State()

    # =====================================================
    # 📝 UMUMIY BUYURTMA MA'LUMOTLARI
    # =====================================================

    waiting_task = State()
    waiting_volume = State()
    waiting_deadline = State()
    waiting_file = State()

    # =====================================================
    # 📑 SAHIFALASH UCHUN MAXSUS BOSQICHLAR
    # =====================================================

    waiting_layout_pages = State()
    waiting_layout_format = State()
    waiting_layout_file_type = State()
    waiting_layout_design = State()
    waiting_layout_deadline = State()
    waiting_layout_file = State()

    # =====================================================
    # 📑 XIZMATGA XOS UMUMIY BOSQICH
    # =====================================================

    waiting_service_details = State()

    # =====================================================
    # 🔍 TASDIQLASH
    # =====================================================

    confirming = State()