import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (title, description) VALUES (?, ?)",
            ('Пётр Первый', 'Последний царь всея Руси')
            )

cur.execute("INSERT INTO users (title, description) VALUES (?, ?)",
            ('Александр Сергеевич Пушкин', 'Великий русский поэт')
            )

connection.commit()
connection.close()