from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'yoursecretkey'  # Required for session

# PostgreSQL Settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:userpassword@db/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    new_task = Task(title=title)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Verifying credentials
        if username == 'admin' and password == 'admin':
            session['username'] = username
            return redirect('/')
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect('/login')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
