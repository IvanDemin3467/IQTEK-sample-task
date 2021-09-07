import sqlite3
from mysql.connector import connect, Error
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

OPTIONS_FILE_PATH = "options.txt"
DB_NAME = "sample_database"


class Repo:
    def __init__(self):
        self.options = self.get_options()
        # self.connection = self.get_db_connection()
        print(self.get_users())

    def get_options(self):
        """
        It reads parameters from file at OPTIONS_FILE_PATH
        Output = dict of options
        """

        options = {"use_db_repo": False, "use_ram_repo": False, "username": None, "password": None,
                   "error": ""}

        try:
            s = open(OPTIONS_FILE_PATH, "rt", encoding="utf-8")
            stream = list(s)
            s.close()
        except:
            options["error"] = "Got exception while reading options from file"
            return options

        for line in stream:
            if line.lstrip().startswith("#"):  # do not read comments
                continue
            line = line.rstrip("\n")
            # read content of string
            fragments = line.split(":")
            # do we use db?
            if "use_db_repo" in fragments[0]:
                if "True" in fragments[1]:
                    options["use_db_repo"] = True
            # do we use db?
            if "use_ram_repo" in fragments[0]:
                if "True" in fragments[1]:
                    options["use_ram_repo"] = True
            # username to connect to db
            elif "username" in fragments[0]:
                options["username"] = fragments[1]
            # password to connect to db
            elif "password" in fragments[0]:
                options["password"] = fragments[1]

        return options

    def get_db_connection(self):
        try:
            return connect(
                    host="localhost",
                    user=self.options["username"],
                    password=self.options["password"],
                    database=DB_NAME,
            )
        except Error as e:
            print(e)

    def make_query(self, query):
        conn = self.get_db_connection()
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
        conn.close()
        if result is None:
            abort(404)
        return result

    def get_user(self, user_id):
        result = self.make_query(f'SELECT * FROM users WHERE id = {user_id}')
        return result

    def get_users(self):
        result = self.make_query('SELECT * FROM users')
        return result

    def add_user(self, title, description):
        result = self.make_query(f"""INSERT INTO users (title, description) 
                                    VALUES ({title}, {description});""")
        return result

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?',
                        (user_id,)).fetchone()
    conn.close()
    if user is None:
        abort(404)
    return user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'gh5ng843bh68hfi4nfc6h3ndh4xc53b56lk89gm4bf2gc6ehm'
repo = Repo()


@app.route('/')
def index():
    # conn = get_db_connection()
    # users = conn.execute('SELECT * FROM users').fetchall()
    # conn.close()
    users = repo.get_users()
    return render_template('index.html', users=users)


@app.route('/<int:user_id>')
def user(user_id):
    # user = get_user(user_id)
    user = repo.get_user(user_id)
    return render_template('user.html', user=user)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (title, description) VALUES (?, ?)',
                         (title, description))
            conn.commit()
            conn.close()
            repo.add_user(title, description)
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    user = get_user(id)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE users SET title = ?, description = ?'
                         ' WHERE id = ?',
                         (title, description, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', user=user)


@app.route('/<int:id>/delete', methods=('GET', 'POST',))
def delete(id):
    user = get_user(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(user['title']))
    return redirect(url_for('index'))


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host="127.0.0.1", port=80)
