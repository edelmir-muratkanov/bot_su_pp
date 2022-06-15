import sqlite3 as sql
from aiogram.dispatcher.storage import FSMContext


def sql_start():
    global base, cur
    base = sql.connect('./data/db.sqlite3')
    cur = base.cursor()

    if base:
        print('DB connected...')

    base.execute('CREATE TABLE IF NOT EXISTS Book (id INTEGER PRIMARY KEY AUTOINCREMENT,chat_id INTEGER NOT NULL,name TEXT NOT NULL,description TEXT,url TEXT NOT NULL)')
    base.execute('CREATE TABLE IF NOT EXISTS Course (id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id INTEGER NOT NULL, name TEXT NOT NULL, description TEXT, url TEXT NOT NULL)')
    base.commit()


async def sql_add_book(state: FSMContext):
    async with state.proxy() as data:
        cur.execute(
            'INSERT INTO Book(chat_id, name, description, url) VALUES (?, ?, ?, ?)',
            tuple(data.values())
        )
        base.commit()


async def sql_select_books(chat_id: int):
    return cur.execute('SELECT name, description, url FROM Book WHERE chat_id = ?', (chat_id,)).fetchall()
