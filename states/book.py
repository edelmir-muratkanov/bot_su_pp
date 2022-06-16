from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message


class BookState(StatesGroup):
    name = State()
    description = State()
    link = State()
