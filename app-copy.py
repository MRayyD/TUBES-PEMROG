from flask import Flask, render_template, redirect, url_for, request, flash, session, g
import pymysql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Database configuration
DB_HOST = 'localhost'
DB_USER = 'your_username'
DB_PASSWORD = 'your_password'
DB_NAME = 'note_app'


# Helper function to get a database connection
def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# Models
class User:
    @staticmethod
    def find_by_username(username):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            return cursor.fetchone()

    @staticmethod
    def find_by_id(user_id):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
            return cursor.fetchone()

    @staticmethod
    def create(username, password):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO user (username, password) VALUES (%s, %s)",
                (username, password)
            )
            db.commit()


class Notebook:
    @staticmethod
    def find_by_user_id(user_id):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM notebook WHERE user_id = %s", (user_id,))
            return cursor.fetchall()

    @staticmethod
    def find_by_id(notebook_id, user_id):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM notebook WHERE id = %s AND user_id = %s",
                (notebook_id, user_id)
            )
            return cursor.fetchone()

    @staticmethod
    def create(title, user_id):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO notebook (title, user_id) VALUES (%s, %s)",
                (title, user_id)
            )
            db.commit()

    @staticmethod
    def delete(notebook_id, user_id):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM note WHERE notebook_id = %s", (notebook_id,))
            cursor.execute(
                "DELETE FROM notebook WHERE id = %s AND user_id = %s",
                (notebook_id, user_id)
            )
            db.commit()


class Note:
    @staticmethod
    def find_by_notebook_id(notebook_id):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM note WHERE notebook_id = %s", (notebook_id,))
            return cursor.fetchall()

    @staticmethod
    def create(content, user_id, notebook_id=None, doodle=None):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO note (content, user_id, notebook_id, doodle) VALUES (%s, %s, %s, %s)",
                (content, user_id, notebook_id, doodle)
            )
            db.commit()

    @staticmethod
    def update(note_id, content, doodle, user_id):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                "UPDATE note SET content = %s, doodle = %s WHERE id = %s AND user_id = %s",
                (content, doodle, note_id, user_id)
            )
            db.commit()

    @staticmethod
    def delete(note_id, user_id):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM note WHERE id = %s AND user_id = %s", (note_id, user_id))
            db.commit()


# Auth Manager
class AuthManager:
    @staticmethod
    def login(username, password):
        user = User.find_by_username(username)
        if user and user['password'] == password:
            session['user_id'] = user['id']
            return True
        return False

    @staticmethod
    def logout():
        session.pop('user_id', None)


# Routes
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    notebooks = Notebook.find_by_user_id(user_id)
    notes = Note.find_by_notebook_id(None)
    return render_template('notes-2.html', notebooks=notebooks, notes=notes)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.find_by_username(username):
            flash('Username already exists.', 'error')
            return redirect(url_for('register'))
        User.create(username, password)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if AuthManager.login(username, password):
            return redirect(url_for('index'))
        flash('Invalid credentials.', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    AuthManager.logout()
    return redirect(url_for('login'))


@app.route('/create_notebook', methods=['POST'])
def create_notebook():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    title = request.form['title']
    Notebook.create(title, session['user_id'])
    flash('Notebook created successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/write_notebook')
def write_notebook():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('write-note.html')

@app.route('/list_notebook')
def list_notebook():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM notebook WHERE user_id = %s", (user_id,))
        notebooks = cursor.fetchall()
        cursor.execute("SELECT * FROM note WHERE user_id = %s", (user_id,))
        notes = cursor.fetchall()
    return render_template('note-list.html', notebooks=notebooks, notes=notes)

@app.route('/add_note', methods=['POST'])
def add_note():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    title = request.form['title']
    content = request.form['note']
    doodle = request.form.get('doodle')
    notebook_id = session.get('current_notebook_id')

    Note.create(content, session['user_id'], notebook_id, doodle)
    flash('Note added successfully!', 'success')
    return redirect(url_for('index' if not notebook_id else 'notebook', notebook_id=notebook_id))

@app.route('/delete_notebook/<int:notebook_id>')
def delete_notebook(notebook_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    Notebook.delete(notebook_id, user_id)
    flash('Notebook deleted successfully!', 'success')
    return render_template('note-list.html')


if __name__ == '__main__':
    app.run(debug=True)
