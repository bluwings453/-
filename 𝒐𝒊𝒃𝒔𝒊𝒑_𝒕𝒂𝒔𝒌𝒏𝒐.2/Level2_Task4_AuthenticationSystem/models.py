from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# The Users table is storing all the Registered Users' data, in a SQLITE3 database
class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(50), unique = False, nullable = True)
    last_name = db.Column(db.String(50), unique = False, nullable = True)
    username = db.Column(db.String(50), unique = False, nullable = True)
    email = db.Column(db.String(100), unique = False, nullable = True)
    password = db.Column(db.Text(200), unique = False, nullable = True)