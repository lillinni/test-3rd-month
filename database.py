import sqlite3

class Database:
    def __init__(self, path: str):
        self.path = path
        self.create_tables()
    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS homeworks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    group_name TEXT NOT NULL,
                    homework_number INTEGER NOT NULL,
                    github_link TEXT NOT NULL
                )
            ''')
            conn.commit()

    def save_homework(self, name, group_name, homework_number, github_link):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO homeworks (name, group_name, homework_number, github_link)
                VALUES (?, ?, ?, ?)
                ''', (name, group_name, homework_number, github_link))
            conn.commit()
