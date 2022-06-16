from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message, ChatActions
from aiogram.dispatcher.storage import FSMContext

from states import BookState
from keyboards.common import ikb_state_cancel
from keyboards.category import ikb_book_category
from loader import dp, db, bot


@dp.callback_query_handler(lambda m: m.data in ['book_category'])
async def show_all_books(query: CallbackQuery):
    books = db.fetchall(
        'SELECT name, description, url FROM Books WHERE chat_id = ?',
        (query.from_user.id,)
    )

    await bot.send_chat_action(query.from_user.id, ChatActions.TYPING)
    if len(books) == 0:
        await query.message.answer('Еще нет карточек', reply_markup=ikb_book_category)

    else:
        for name, desc, url in books:
            if name == books[-1][0]:
                await query.message.answer(
                    '<b><a href="{}">{}</a></b>\n{}'.format(url, name, desc),
                    reply_markup=ikb_book_category
                )
            else:
                await bot.send_message(
                    query.from_user.id,
                    '<b><a href="{}">{}</a></b>\n{}'.format(url, name, desc)
                )


@dp.callback_query_handler(lambda m: m.data in ['append_book_card'])
async def append_book(query: CallbackQuery):
    await BookState.name.set()
    await bot.send_message(query.from_user.id, 'Введите название книги: ', reply_markup=ikb_state_cancel)


@dp.message_handler(state=BookState.name)
async def book_name_state(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await BookState.next()
    await bot.send_message(message.from_user.id, 'Введите описание книги: ', reply_markup=ikb_state_cancel)


@dp.message_handler(state=BookState.description)
async def book_desc_state(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

    await BookState.next()
    await bot.send_message(message.from_user.id, 'Введите ссылку на книгу: ', reply_markup=ikb_state_cancel)


@dp.message_handler(state=BookState.link)
async def book_link_state(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['link'] = message.text

    await db.query(
        'INSERT INTO Books (chat_id, name, description, link) VALUES (?, ?, ?, ?)',
        (message.from_user.id, data['name'], data['description'], data['link'])
    )

    await bot.send_message(
        message.from_user.id,
        'Книга успешно добавлена',
        reply_markup=ikb_book_category
    )

    await state.finish()
