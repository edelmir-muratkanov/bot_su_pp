from aiogram.types import InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup


def create_ikb_category(name: str, data_name: str):

    return Markup(
        row_width=1,
        inline_keyboard=[
            [Button(f'Добавить {name.lower()}',
                    callback_data=f'append_{data_name}_card')],
            [Button(f'Назад', callback_data=f'{data_name}_category_return')]
        ]
    )


ikb_book_category = create_ikb_category('книгу', 'book')
ikb_course_category = create_ikb_category('курс', 'course')
