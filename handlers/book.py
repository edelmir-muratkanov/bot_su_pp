from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


from data.db import sql_add_book, sql_select_books
from keyboards.common import ikb_state_cancel
from keyboards.category import ikb_book_category
from loader import dp, bot


class Book(StatesGroup):
    name = State()
    description = State()
    link = State()


@dp.callback_query_handler(lambda m: m.data in ['book_category'])
async def show_all_books(query: CallbackQuery):
    books = await sql_select_books(query.from_user.id)

    for b in books:
        name, desc, url = b
        if b == books[-1]:
            await bot.send_message(
                query.from_user.id,
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
    await Book.name.set()
    await bot.send_message(query.from_user.id, 'Введите название книги: ', reply_markup=ikb_state_cancel)


@dp.message_handler(state=Book.name)
async def book_name_state(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['chat_id'] = message.from_user.id
        data['name'] = message.text

    await Book.next()
    await bot.send_message(message.from_user.id, 'Введите описание книги: ', reply_markup=ikb_state_cancel)


@dp.message_handler(state=Book.description)
async def book_desc_state(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

    await Book.next()
    await bot.send_message(message.from_user.id, 'Введите ссылку на книгу: ', reply_markup=ikb_state_cancel)


@dp.message_handler(state=Book.link)
async def book_link_state(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['link'] = message.text

    await sql_add_book(state)

    await bot.send_message(
        message.from_user.id,
        'Книга успешно добавлена',
        reply_markup=ikb_book_category
    )

    await state.finish()
