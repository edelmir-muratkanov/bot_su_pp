from aiogram.dispatcher.filters.state import State, StatesGroup


class BookState(StatesGroup):
    name = State()
    description = State()
    link = State()
