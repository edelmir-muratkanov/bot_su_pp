from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


book_card_cb = CallbackData('book_card', 'id', 'action')
book_category_cb = CallbackData('book_category', 'action')

course_card_cb = CallbackData('course_card', 'id', 'action')
course_category_cb = CallbackData('course_category', 'action')

youtube_card_cb = CallbackData('youtube_card', 'id', 'action')
youtube_category_cb = CallbackData('youtube_category', 'action')

storage_state_cb = CallbackData('state', 'action')


def _create_card_markup(cb: CallbackData, idx):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            'Удалить карточку',
            callback_data=cb.new(id=idx, action='remove')
        )
    )

    return markup


def _create_category_markup(cb: CallbackData):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            'Все карточки',
            callback_data=cb.new(action='view')
        ),
        InlineKeyboardButton(
            'Добавить карточку',
            callback_data=cb.new(action='append')
        )
    )

    return markup


def storage_state_cancel_markup():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            'Отменить',
            callback_data=storage_state_cb.new(action='cancel')
        )
    )
    return markup


def book_card_markup(idx):
    return _create_card_markup(book_card_cb, idx)


def book_category_markup():
    return _create_category_markup(book_category_cb)


def course_card_markup(idx):
    return _create_card_markup(course_card_cb, idx)


def course_category_markup():
    return _create_category_markup(course_category_cb)


def youtube_card_markup(idx):
    return _create_card_markup(youtube_card_cb, idx)


def youtube_category_markup():
    return _create_category_markup(youtube_category_cb)
