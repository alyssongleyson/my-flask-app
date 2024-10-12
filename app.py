from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# PostgreSQL Settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:userpassword@db/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the task table template
class Task(db.Model):
	id = db.Column(db.Integer, primay_key=True)
	title = db.Column(db.String(255), nullable=False)

@app.route('/')
def inde():
	tasks = Task.query.all()
	return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
	if request.method == 'POST':
	title = request.form['title']
	new_task = Task(title=title)
	db.session.add(new_task)
	db.session.commit()
	return redirect('/')

if __name__ == '__main__':
	db.create_all() #Create tables in the database
	app.run(debug=True, host='0.0.0.0')

@app.route('/delete/<int:id>')
def delete_task(id):
	task = Task.query.get(id)
	if task:
		db.session.delete(task)
		db.session.commit()
	return redirect('/')
