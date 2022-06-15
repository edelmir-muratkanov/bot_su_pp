from aiogram import Dispatcher, executor

from data.db import sql_start
from keyboards import *
from handlers import dp


async def on_startup(dp: Dispatcher):
    sql_start()
    print('Bot enabled')


async def on_shutdown(dp: Dispatcher):
    dp.storage.close()
    dp.storage.wait_closed()
    print('Bot disabled')


if __name__ == '__main__':
    executor.start_polling(
        dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True
    )
