from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://your_username:your_password@localhost/note_app'
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2:sha256'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Notebook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=True)  # Store the content as text
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('notes.html', notes=notes)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your username and/or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add_note', methods=['POST'])
@login_required 
def add_note():
    note_content = request.form['note']
    new_note = Note(content=note_content, user_id=current_user.id)
    db.session.add(new_note)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_note/<int:note_id>')
@login_required
def delete_note(note_id):
    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/notebooks')
@login_required
def notebooks():
    notebooks = Notebook.query.filter_by(user_id=current_user.id).all()
    return render_template('view_notebooks.html', notebooks=notebooks)

@app.route('/notebook/<int:notebook_id>', methods=['GET', 'POST'])
@login_required
def notebook(notebook_id):
    notebook = Notebook.query.get_or_404(notebook_id)
    if notebook.user_id != current_user.id:
        flash("You do not have access to this notebook.")
        return redirect(url_for('notebooks'))

    if request.method == 'POST':
        notebook.content = request.form['content']
        db.session.commit()
        flash('Notebook updated successfully!')
        return redirect(url_for('notebook', notebook_id=notebook.id))

    return render_template('notebook.html', notebook=notebook)

@app.route('/create_notebook', methods=['POST'])
@login_required
def create_notebook():
    if request.method == 'POST':

        title = request.form['title']
        new_notebook = Notebook(title=title, user_id=current_user.id)
        db.session.add(new_notebook)
        db.session.commit()
        return redirect(url_for('notebooks'))

    return render_template('create_notebook.html')  # Render the form for creating a notebook

@app.route('/delete_notebook/<int:notebook_id>')
@login_required
def delete_notebook(notebook_id):
    notebook = Notebook.query.get(notebook_id)
    if notebook and notebook.user_id == current_user.id:
        db.session.delete(notebook)
        db.session.commit()
    return redirect(url_for('notebooks'))

with app.app_context():
    db.create_all()  # This will create the tables in the database

if __name__ == "__main__":
    app.run(debug=True)