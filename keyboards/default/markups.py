from aiogram.types import ReplyKeyboardMarkup


all_cards = '🧮 Все карточки'
categories = '🗄 Категории'


def start_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(all_cards, categories)

    return markup


def categories_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row('Книги', 'Курсы')
    markup.add('Youtube')

    return markup
