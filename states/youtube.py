from aiogram.dispatcher.filters.state import State, StatesGroup


class YoutubeState(StatesGroup):
    link = State()
