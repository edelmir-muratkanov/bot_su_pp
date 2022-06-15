from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext

from keyboards.common import *
from loader import dp, bot


@dp.callback_query_handler(lambda m: m.data in ['show_all_cards_return', 'show_all_categories_return'])
@dp.message_handler(commands=['start'])
async def cmd_start(message: Message = None, query: CallbackQuery = None):
    chat_id = None
    if not message and not query:
        return
    if message:
        chat_id = message.from_user.id
    if query:
        chat_id = query.from_user.id

    await bot.send_message(
        chat_id,
        f'Добро пожаловать {message.from_user.full_name}',
        reply_markup=ikb_start
    )


@dp.callback_query_handler(lambda m: m.data in ['show_all_cards'])
async def show_all_cards(query: CallbackQuery):
    await bot.send_message(
        query.from_user.id,
        'все карточки',
        reply_markup=ikb_show_all_cards
    )


@dp.callback_query_handler(lambda m: m.data in ['show_all_categories', 'book_category_return'])
# @dp.callback_query_handler(lambda m: m.data == 'show_all_categories')
async def show_all_categories(query: CallbackQuery):
    await bot.send_message(
        query.from_user.id,
        'Категории',
        reply_markup=ikb_show_all_categories
    )


@dp.message_handler(state='*', commands='cancel')
@dp.callback_query_handler(lambda m: m.data in ['cancel'], state='*')
async def cmd_cancel(message: Message = None, query: CallbackQuery = None, state: FSMContext = None):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

    chat_id = None
    if not message and not query:
        return
    if message:
        chat_id = message.from_user.id
    if query:
        chat_id = query.from_user.id

    await bot.send_message(chat_id, 'Отменено', reply_markup=ikb_start)
