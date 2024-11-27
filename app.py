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

# Routes
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM notebook WHERE user_id = %s", (user_id,))
        notebooks = cursor.fetchall()
        cursor.execute("SELECT * FROM note WHERE user_id = %s", (user_id))
        notes = cursor.fetchall()
    return render_template('notes.html', notebooks=notebooks, notes=notes)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT id FROM user WHERE username = %s", (username,))
            if cursor.fetchone():
                flash('Username already exists.', 'error')
                return redirect(url_for('register'))

            cursor.execute(
                "INSERT INTO user (username, password) VALUES (%s, %s)",
                (username, password)
            )
            db.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM user WHERE username = %s AND password = %s",
                (username, password)
            )
            user = cursor.fetchone()
            if user:
                session['user_id'] = user['id']
                return redirect(url_for('index'))
            flash('Invalid credentials.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/create_notebook', methods=['POST'])
def create_notebook():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    title = request.form['title']
    user_id = session['user_id']

    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            "INSERT INTO notebook (title, user_id) VALUES (%s, %s)",
            (title, user_id)
        )
        db.commit()
    flash('Notebook created successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/notebook/<int:notebook_id>')
def notebook(notebook_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM notebook WHERE id = %s AND user_id = %s", (notebook_id, user_id))
        notebook = cursor.fetchone()
        if not notebook:
            flash('Notebook not found or access denied.', 'error')
            return redirect(url_for('index'))
        
        cursor.execute("SELECT * FROM note WHERE notebook_id = %s", (notebook_id))
        note = cursor.fetchall()
    
    session['current_notebook_id'] = notebook_id
    return render_template('notebook.html', notebook=notebook, note=note)

@app.route('/add_note', methods=['POST'])
def add_note():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    note_content = request.form['note']
    note_doodle = request.form['doodle']
    notebook_id = session.get('current_notebook_id')
    user_id = session['user_id']

    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            "INSERT INTO note (content, user_id, doodle, notebook_id) VALUES (%s, %s, %s, %s)",
            (note_content, user_id, note_doodle, notebook_id)
        )
        db.commit()
    flash('Note added successfully!', 'success')
    return redirect(url_for('index' if not notebook_id else 'notebook', notebook_id=notebook_id))

@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    notebook_id = session.get('current_notebook_id')

    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM note WHERE id = %s AND user_id = %s", (note_id, user_id))
        db.commit()
    flash('Note deleted successfully!', 'success')
    return redirect(url_for('index' if not notebook_id else 'notebook', notebook_id=notebook_id))

@app.route('/delete_notebook/<int:notebook_id>')
def delete_notebook(notebook_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM note WHERE notebook_id = %s", (notebook_id,))
        cursor.execute("DELETE FROM notebook WHERE id = %s AND user_id = %s", (notebook_id, user_id))
        db.commit()
    flash('Notebook deleted successfully!', 'success')
    return redirect(url_for('index'))

# Database setup script
@app.before_request
def setup_database():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(150) UNIQUE NOT NULL,
            password CHAR(64) NOT NULL
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS notebook (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(150) NOT NULL,
            user_id INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user(id)
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS note (
            id INT AUTO_INCREMENT PRIMARY KEY,
            content VARCHAR(500) NOT NULL,
            user_id INT NOT NULL,
            notebook_id INT DEFAULT NULL,
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (notebook_id) REFERENCES notebook(id)
        );
        """)
        db.commit()

if __name__ == '__main__':
    app.run(debug=True)