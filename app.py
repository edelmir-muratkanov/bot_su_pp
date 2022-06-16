import logging
import os
from aiogram import Dispatcher, executor, types

from data.config import APP_HOST, WEBHOOK_PATH, WEBHOOK_URL
from keyboards.default import markups
from loader import bot, dp, db
import handlers


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.answer('~~Привет~~\nЯ бот хранитель знаний.\nПользуйтесь клавиатурой.\nКоманда help бесполезна 😁.', reply_markup=markups.start_markup())


async def on_startup(dp: Dispatcher):
    logging.basicConfig(level=logging.INFO)
    logging.info('Bot is starting...')

    db.create_tables()

    await dp.bot.delete_webhook()
    await dp.bot.set_webhook(WEBHOOK_URL)

    logging.info('Bot is online')


async def on_shutdown(dp: Dispatcher):
    logging.warning('Bot is shutting down...')

    await dp.bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bot is down')


if __name__ == '__main__':

    if 'HEROKU' in list(os.environ.keys()):
        executor.start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=APP_HOST,
            port=APP_HOST
        )
    else:
        executor.start_polling(
            dispatcher=dp,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True
        )
