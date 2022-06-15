from aiogram.dispatcher.filters.state import State, StatesGroup


class Youtube(StatesGroup):
    link = State()
