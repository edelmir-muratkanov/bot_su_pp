import logging
from loader import dp, db, bot
from aiogram.types import CallbackQuery, ChatActions, Message
from aiogram.dispatcher.storage import FSMContext
from keyboards.inline import markups
from states import *


@dp.callback_query_handler(markups.storage_state_cb.filter(action='cancel'), state='*')
async def cancel_storage_state_callback(query: CallbackQuery, state: FSMContext):
    logging.debug('CANCEL')

    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await query.answer('Отменено')


# BOOK

@dp.callback_query_handler(markups.book_card_cb.filter(action='remove'))
async def remove_card_book_callback(query: CallbackQuery, callback_data: dict):
    db.query('DELETE FROM Books WHERE id = ?', (callback_data['id'],))
    await query.answer('Карточка успешно удалена')
    await query.message.delete()


@dp.callback_query_handler(markups.book_category_cb.filter(action='view'))
async def view_cards_book_callback(query: CallbackQuery):
    items = db.fetchall(
        'SELECT id, name, description, url FROM Books WHERE chat_id = ?',
        (query.from_user.id,)
    )
    if len(items) == 0:
        await query.message.answer('Карточек нет')
        await query.message.delete()
    else:
        await bot.send_chat_action(query.from_user.id, ChatActions.TYPING)
        for id, name, description, url in items:
            await query.message.answer(
                "<b><a href='{}'>{}</a></b>\n{}".format(
                    url, name, description),
                reply_markup=markups.book_card_markup(id)
            )
        await query.message.delete()


@dp.callback_query_handler(markups.book_category_cb.filter(action='append'))
async def add_card_book_callback(query: CallbackQuery):
    await BookState.name.set()
    await query.message.answer('Введите название книги: ', reply_markup=markups.storage_state_cancel_markup())
    await query.message.delete()


@dp.message_handler(state=BookState.name)
async def set_book_name_state(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await BookState.next()
    await message.answer('Введите описание книги: ', reply_markup=markups.storage_state_cancel_markup())


@dp.message_handler(state=BookState.description)
async def set_book_description_state(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

    await BookState.next()
    await message.answer('Введите ссылку на книгу: ', reply_markup=markups.storage_state_cancel_markup())


@dp.message_handler(state=BookState.link)
async def set_book_link_state(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['link'] = message.text

    db.query(
        'INSERT INTO Books (chat_id, name, description, url) VALUES (?, ?, ?, ?)',
        (message.from_user.id, data['name'], data['description'], data['link'])
    )
    await message.answer('Книга успешно добавлена')
    await state.finish()


# COURSE


@dp.callback_query_handler(markups.course_category_cb.filter(action='view'))
async def view_cards_course_callback(query: CallbackQuery):
    items = db.fetchall(
        'SELECT id, name, description, url FROM Courses WHERE chat_id = ?',
        (query.from_user.id,)
    )
    if len(items) == 0:
        await query.message.answer('Карточек нет')
        await query.message.delete()
    else:
        await bot.send_chat_action(query.from_user.id, ChatActions.TYPING)
        for id, name, description, url in items:
            await query.message.answer(
                "<b><a href='{}'>{}</a></b>\n{}".format(
                    url, name, description),
                reply_markup=markups.course_card_cb(id)
            )
        await query.message.delete()


@dp.callback_query_handler(markups.course_card_cb.filter(action='remove'))
async def remove_card_course_callback(query: CallbackQuery, callback_data: dict):
    db.query('DELETE FROM Courses WHERE id = ?', (callback_data['id'],))
    await query.answer('Карточка успешно удалена')
    await query.message.delete()


@dp.callback_query_handler(markups.course_category_cb.filter(action='append'))
async def add_card_course_callback(query: CallbackQuery):
    await CourseState.name.set()
    await query.message.answer('Введите название курса: ', reply_markup=markups.storage_state_cancel_markup())
    await query.message.delete()


@dp.message_handler(state=CourseState.name)
async def set_course_name_state(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await CourseState.next()
    await message.answer('Введите описание курса: ', reply_markup=markups.storage_state_cancel_markup())


@dp.message_handler(state=CourseState.description)
async def set_course_description_state(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

    await CourseState.next()
    await message.answer('Введите ссылку на курс: ', reply_markup=markups.storage_state_cancel_markup())


@dp.message_handler(state=CourseState.link)
async def set_course_link_state(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['link'] = message.text

    db.query(
        'INSERT INTO Courses (chat_id, name, description, url) VALUES (?, ?, ?, ?)',
        (message.from_user.id, data['name'], data['description'], data['link'])
    )
    await message.answer('Курс успешно добавлен')
    await state.finish()


# YOUTUBE

@dp.callback_query_handler(markups.youtube_category_cb.filter(action='view'))
async def view_cards_youtube_callback(query: CallbackQuery):
    items = db.fetchall(
        'SELECT * FROM Youtubes WHERE chat_id = ?',
        (query.from_user.id, )
    )
    if len(items) == 0:
        await query.message.answer('Карточек нет')
        await query.message.delete()
    else:
        await bot.send_chat_action(query.from_user.id, ChatActions.TYPING)
        for id, chat_id, url in items:
            await query.message.answer(url, reply_markup=markups.youtube_card_markup(id))
        await query.message.delete()


@dp.callback_query_handler(markups.youtube_card_cb.filter(action='remove'))
async def remove_card_youtube_callback(query: CallbackQuery, callback_data: dict):
    db.query('DELETE FROM Youtubes WHERE id = ?', (callback_data['id'],))
    await query.answer('Карточка успешно удалена')
    await query.message.delete()


@dp.callback_query_handler(markups.youtube_category_cb.filter(action='append'))
async def add_youtube_course_callback(query: CallbackQuery):
    await YoutubeState.link.set()
    await query.message.answer('Введите ссылку на youtube видео: ', reply_markup=markups.storage_state_cancel_markup())
    await query.message.delete()


@dp.message_handler(state=YoutubeState.link)
async def set_youtube_link_state(message: Message, state: FSMContext):
    db.query('INSERT INTO youtubes (chat_id, url) VALUES (?, ?)',
             (message.from_user.id, message.text))
    await message.answer('Видео успешно добавлено')
    await state.finish()
