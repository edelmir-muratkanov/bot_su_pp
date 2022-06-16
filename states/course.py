from aiogram.dispatcher.filters.state import State, StatesGroup


class CourseState(StatesGroup):
    name = State()
    description = State()
    link = State()
