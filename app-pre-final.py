from flask import Flask, render_template, redirect, url_for, request, flash, session, g
from flask_socketio import SocketIO, emit, join_room, leave_room
import pymysql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

socketio = SocketIO(app, async_mode='eventlet')

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
    def create(content, user_id, notebook_id, doodle=None):
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

@socketio.on('connect')
def handle_connect():
    """Handle new socket connection."""
    if 'user_id' not in session:
        return False
    

@socketio.on('join_notebook')
def on_join_notebook(data):
    """Allow users to join a notebook's real-time room."""
    if 'user_id' not in session:
        return False
    
    notebook_id = data.get('notebook_id')
    room = f'notebook_{notebook_id}'
    join_room(room)
    
    # Fetch current notes for the notebook
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM note WHERE notebook_id = %s ORDER BY id DESC", 
            (notebook_id,)
        )
        notes = cursor.fetchall()
    
    # Emit existing notes to the joining user
    emit('notebook_notes', {'notes': notes})


@socketio.on('leave_notebook')
def on_leave_notebook(data):
    """Allow users to leave a notebook's real-time room."""
    notebook_id = data.get('notebook_id')
    room = f'notebook_{notebook_id}'
    leave_room(room)


@socketio.on('create_collaborative_note')
def handle_create_collaborative_note(data):
    """Handle real-time note creation with collaborative features."""
    if 'user_id' not in session:
        return False
    
    user_id = session['user_id']
    notebook_id = data.get('notebook_id')
    content = data.get('content')
    doodle = data.get('doodle', None)
    
    try:
        # Create note
        Note.create(content, user_id, notebook_id, doodle)
        
        # Get the newly created note with its ID
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM note WHERE content = %s AND user_id = %s AND notebook_id = %s ORDER BY id DESC LIMIT 1", 
                (content, user_id, notebook_id)
            )
            new_note = cursor.fetchone()
        
        # Broadcast the new note to all users in the notebook room
        room = f'notebook_{notebook_id}'
        emit('new_note', {'note': new_note}, room=room)
        
        return {'status': 'success', 'note': new_note}
    
    except Exception as e:
        app.logger.error(f"Socket note creation error: {e}")
        return {'status': 'error', 'message': str(e)}


@socketio.on('update_collaborative_note')
def handle_update_collaborative_note(data):
    """Handle real-time note updates with collaborative features."""
    if 'user_id' not in session:
        return False
    
    user_id = session['user_id']
    note_id = data.get('note_id')
    content = data.get('content')
    doodle = data.get('doodle', None)
    notebook_id = data.get('notebook_id')
    
    try:
        # Update note
        Note.update(note_id, content, doodle, user_id)
        
        # Broadcast the updated note to all users in the notebook room
        room = f'notebook_{notebook_id}'
        emit('note_updated', {
            'note_id': note_id, 
            'content': content, 
            'doodle': doodle
        }, room=room)
        
        return {'status': 'success'}
    
    except Exception as e:
        app.logger.error(f"Socket note update error: {e}")
        return {'status': 'error', 'message': str(e)}

# Routes
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    notebooks = Notebook.find_by_user_id(user_id)
    notes = Note.find_by_notebook_id(None)
    return render_template('notes-index.html', notebooks=notebooks, notes=notes)


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

@app.route('/write_notebook')
def write_notebook():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    notebooks = Notebook.find_by_user_id(user_id)
    return render_template('write-note.html', notebooks=notebooks, socketio_enabled=True)

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
    return render_template('note-list.html', notebooks=notebooks, notes=notes, socketio_enabled=True)

@app.route('/delete_notebook/<int:notebook_id>')
def delete_notebook(notebook_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    Notebook.delete(notebook_id, user_id)
    flash('Notebook deleted successfully!', 'success')
    return redirect(url_for('list_notebook'))

@app.route('/add_note', methods=['POST'])
def add_note():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    notebook_name = request.form.get('notebook_name')
    content = request.form.get('note')
    doodle = request.form.get('doodle')

    if not notebook_name or not content:
        flash('Notebook name, title, and note content are required.', 'error')
        return redirect(url_for('write_notebook'))

    try:
        # Check if notebook exists
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM notebook WHERE title = %s AND user_id = %s",
                (notebook_name, user_id)
            )
            notebook = cursor.fetchone()

        # Create notebook if it doesn't exist
        if not notebook:
            Notebook.create(notebook_name, user_id)
            with db.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM notebook WHERE title = %s AND user_id = %s",
                    (notebook_name, user_id)
                )
                notebook = cursor.fetchone()

        notebook_id = notebook['id']

        # Add the note
        Note.create(content, user_id, notebook_id, doodle)
        flash('Note and notebook added successfully!', 'success')

    except Exception as e:
        app.logger.error(f"Error saving note: {e}")
        flash('Failed to add note. Please try again.', 'error')

    return redirect(url_for('list_notebook'))


@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    Note.delete(note_id, user_id)
    flash('Note deleted successfully!', 'success')
    return redirect(url_for('list_notebook'))



if __name__ == '__main__':
    socketio.run(app, debug=True)
