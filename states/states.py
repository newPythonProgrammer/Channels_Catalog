from aiogram.dispatcher.filters.state import State, StatesGroup

class FSM_ADMIN_SPAM(StatesGroup):
    text = State()
    btns = State()

class EDIT_TEXT(StatesGroup):
    text_id = State()
    text = State()