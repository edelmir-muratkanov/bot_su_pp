import sqlite3 as sql


class DatabaseManager:

    def __init__(self, path):
        self.conn = sql.connect(path)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    def create_tables(self):
        self.query('CREATE TABLE IF NOT EXISTS Books (id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id INTEGER NOT NULL,name TEXT NOT NULL,description TEXT,url TEXT NOT NULL)')
        self.query('CREATE TABLE IF NOT EXISTS Courses (id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id INTEGER NOT NULL, name TEXT NOT NULL, description TEXT, url TEXT NOT NULL)')
        self.query(
            'CREATE TABLE IF NOT EXISTS Youtubes (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT NOT NULL)')

    def query(self, arg, values=None):
        if values is None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)

        self.conn.commit()

    def fetchone(self, arg, values=None):
        if values is None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)

        return self.cur.fetchone()

    def fetchall(self, arg, values=None):
        if values is None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)

        return self.cur.fetchall()

    def __del__(self):
        self.conn.close()


"""
====== Books ======
id          INTEGER
chat_id     INTEGER
name        TEXT
description TEXT
url         TEXT

====== Courses ======
id          INTEGER
chat_id     INTEGER
name        TEXT
description TEXT
url         TEXT

=== Youtubes ===
id      INTEGER
url     TEXT
"""
