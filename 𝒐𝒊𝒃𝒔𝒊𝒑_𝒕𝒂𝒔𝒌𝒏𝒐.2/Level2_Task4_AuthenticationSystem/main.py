'''
Create a simple login authentication system using a programming language of your choice (e.g., Python, JavaScript, 
Java, etc.) that allows users to register, login, and access a secured page.
'''

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from models import db, Users

# from termcolor import colored

app = Flask(__name__, template_folder = 'templates', static_folder = 'static')

# Configurations for connecting to sqlite3 database.
app.config.update(
	SQLALCHEMY_DATABASE_URI = "sqlite:///users.db",
	SECRET_KEY = "TheRandomKey",
)

# Automatically migrate defined models to database if not done already.
db.init_app(app)
migrate = Migrate(app, db)

# Home page -> user will see only the login or signup options if not logged in else will see the logout button and the content about the task 
@app.route("/")
def home():
	if 'username' in session:
		return render_template('index.html', username = session['username'])
	else:
		return render_template('index.html')
	
# Sign Up page -> users can regster themselves here, if not already, by entering their First Name, Last Name, Email, Username and Password.
# NOTE: The password will be hashed before saving to database, so that there is no security risk.
@app.route("/user-signup", methods = ['GET', 'POST'])
def register():
	if 'username' not in session:
		if request.method == 'POST':
			first_name = request.form['first_name']
			last_name = request.form['last_name']
			username = request.form['username']
			email = request.form['email']
			password = request.form['password']
			if Users.query.filter_by(email = email).first() is not None:
				flash(message = "Email Already Registered", category = "error")
				# print(colored("Email Already Registered", "red"))
				return redirect(url_for('register'))
			elif Users.query.filter_by(username = username).first() is not None:
				flash(message = "Username Already Exists", category = "error")
				# print(colored("Username Already Exists", "red"))
				return redirect(url_for('register'))
			else:
				user = Users(first_name = first_name, last_name = last_name, username = username, email = email, password = generate_password_hash(password))
				db.session.add(user)
				db.session.commit()
				# print(colored("Registration Successful", "green"))
				return redirect(url_for('login'))
		return render_template('register.html')
	else:
		return redirect(url_for('home'))

# Login page -> users can login to see the secured page content Username and Password
@app.route("/user-login", methods = ['GET', 'POST'])
def login():
	if 'username' not in session: 
		if request.method == 'POST':
			username = request.form['username']
			password = request.form['password']
			user = Users.query.filter_by(username = username).first()
			if user is not None:
				searched_password = user.password
				if check_password_hash(pwhash = searched_password, password = password):
					# print(colored("Login Successful", "green"))
					session['username'] = username
					return redirect(url_for('home'))
				else:
					flash(message = "wrong password", category = "error")
					# print(colored("Login Failed", "red"))
					return redirect(url_for('login'))
			else:
				flash(message = "wrong username or password", category = "error")
				# print(colored("Login Failed", "red"))
				return redirect(url_for('login'))
		return render_template('login.html')
	else:
		return redirect(url_for('home'))
	
# User will get logged out by simply clicking the logout button once
@app.route("/logout")
def logout():
	session.pop("username", None)
	# print(colored("Logout Successful", "green"))
	return redirect(url_for('home'))

if __name__ == '__main__':
	app.run()
