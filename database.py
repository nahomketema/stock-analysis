'''
Nahom Ketema
database.py

This file is currently under development so it will not be necessary until later updates
'''

from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site_data.db"
db = SQLAlchemy()
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.password}')"

#db.create_all()

#after everything is done, add a db.init_app(app)