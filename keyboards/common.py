from aiogram.types import InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup

ikb_start = Markup(
    row_width=1,
    inline_keyboard=[
        [
            Button(
                'Показать все карточки',
                callback_data='show_all_cards'
            ),

        ],
        [
            Button(
                'Показать все категории',
                callback_data='show_all_categories'
            )
        ]

    ]
)

ikb_show_all_cards = Markup(
    row_width=1,
    inline_keyboard=[
        [
            Button(
                'Назад',
                callback_data='show_all_cards_return'
            )
        ]
    ]
)


ikb_show_all_categories = Markup(
    row_width=2,
    inline_keyboard=[
        [

            Button(
                'Книги',
                callback_data='book_category'
            ),
            Button(
                'Курсы',
                callback_data='course_category'
            ),
            Button(
                'Назад',
                callback_data='show_all_categories_return'
            ),
        ]
    ]
)


ikb_state_cancel = Markup(
    row_width=1,
    inline_keyboard=[
        [
            Button('Отмена', callback_data='cancel')
        ]
    ]
)
