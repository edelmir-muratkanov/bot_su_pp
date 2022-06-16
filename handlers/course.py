from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext

from states import CourseState
from keyboards.category import ikb_course_category
from loader import dp, bot


@dp.callback_query_handler(lambda m: m.data in ['course_category'])
async def show_all_books(query: CallbackQuery):
    await bot.send_message(
        query.from_user.id,
        'Курсы',
        reply_markup=ikb_course_category
    )


@dp.callback_query_handler(lambda m: m.data in ['append_course_card'])
async def append_book(query: CallbackQuery):
    await CourseState.name.set()
    await bot.send_message(query.from_user.id, 'Введите название курса: ')


@dp.message_handler(state=CourseState.name)
async def course_name_state(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['chat_id'] = message.from_user.id
        data['name'] = message.text

    await CourseState.next()
    await bot.send_message(message.from_user.id, 'Введите описание курса: ')


@dp.message_handler(state=CourseState.description)
async def course_desc_state(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

    await CourseState.next()
    await bot.send_message(message.from_user.id, 'Введите ссылку на книгу: ')


@dp.message_handler(state=CourseState.link)
async def course_link_state(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['link'] = message.text

    await bot.send_message(
        message.from_user.id,
        'Курс: <b><a href="{}">{}</a></b>\n'.format(data['link'], data['name']) +
        'Описание: {}\n\n'.format(data['description']),
        reply_markup=ikb_course_category
    )

    await state.finish()
