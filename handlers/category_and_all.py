from email import message
from aiogram.types import Message, ChatActions

from loader import dp, db, bot
from keyboards.default import markups as dmk
from keyboards.inline import markups as imk


@dp.message_handler(text=dmk.all_cards)
async def all_cards(message: Message):
    books = db.fetchall(
        'SELECT * FROM Books WHERE chat_id = ?',
        (message.from_user.id,)
    )
    courses = db.fetchall(
        'SELECT * FROM Courses WHERE chat_id = ?',
        (message.from_user.id, )
    )
    youtubes = db.fetchall(
        'SELECT * FROM Youtubes WHERE chat_id = ?',
        (message.from_user.id, )
    )

    if not len(books) and not len(courses) and not len(youtubes):
        await message.answer('Карточек нет')
    else:
        await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
        for id, _, name, description, url in books:
            await message.answer(
                "<b><a href={}>{}</a></b>\n{}".format(url, name, description),
                reply_markup=imk.book_card_markup(id)
            )
        for id, _, name, description, url in books:
            await message.answer(
                "<b><a href={}>{}</a></b>\n{}".format(url, name, description),
                reply_markup=imk.course_card_markup(id)
            )
        for id, url in youtubes:
            await message.answer(url, reply_markup=imk.youtube_card_markup)


@dp.message_handler(text=dmk.categories)
async def categories(message: Message):
    await message.answer('Выберите категорию: ', reply_markup=dmk.categories_markup())


@dp.message_handler(text='Книги')
async def book_category(message: Message):
    await message.answer('Что вы хотите?', reply_markup=imk.book_category_markup())


@dp.message_handler(text='Курсы')
async def course_category(message: Message):
    await message.answer('Что вы хотите?', reply_markup=imk.book_category_markup())


@dp.message_handler(text='Youtube')
async def youtube_category(message: Message):
    await message.answer('Что вы хотите?', reply_markup=imk.youtube_category_markup())
