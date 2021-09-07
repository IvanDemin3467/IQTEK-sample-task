import mysql.connector as mysql
from mysql.connector import connect, Error
import app

# connection = sqlite3.connect('database.db')
# connection = mysql.connect(
#             host="localhost",
#             user=app.repo.options["username"],
#             password=app.repo.options["password"],
#             #database=app.DB_NAME,
#             )


try:
    with connect(
            host="localhost",
            user=app.repo.options["username"],
            password=app.repo.options["password"]
            ) as connection:
        create_db_query = f"CREATE DATABASE {app.DB_NAME};"
        print(create_db_query)
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)
except Error as e:
    print(e)

# with open('schema.sql') as f:
#     connection.executescript(f.read())

# cur = connection.cursor()
#
# cur.execute("INSERT INTO users (title, description) VALUES (?, ?)",
#             ('Пётр Первый', 'Последний царь всея Руси')
#             )
#
# cur.execute("INSERT INTO users (title, description) VALUES (?, ?)",
#             ('Александр Сергеевич Пушкин', 'Великий русский поэт')
#             )
#
# connection.commit()
# connection.close()