from aiogram.fsm.state import State, StatesGroup


class PriceStates(StatesGroup):
    waiting_service_name = State()
    waiting_price = State()
    waiting_description = State()


class PaymentStates(StatesGroup):
    waiting_order_price = State()
class PaymentSettingStates(StatesGroup):
    waiting_method_details = State()