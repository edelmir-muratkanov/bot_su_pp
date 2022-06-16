from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

category_cb = CallbackData('category', 'action')

def category_markup():
    
    global category_cb
    
    markup = InlineKeyboardMarkup()
    for id, title in [(1, 'Книги'), (2, 'Курсы')]:
        markup.add(InlineKeyboardButton('Добавить '))
