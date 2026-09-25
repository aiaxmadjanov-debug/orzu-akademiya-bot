from aiogram.fsm.state import State, StatesGroup


class ContestStates(StatesGroup):
    waiting_name = State()
    waiting_phone = State()
    waiting_contest = State()
    waiting_description = State()
    waiting_file = State()
    confirming = State()