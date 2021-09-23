from aiogram.dispatcher.filters.state import State, StatesGroup

class GetIDs(StatesGroup):
    channel = State()
    user_info = State()