# Where we create the database models. 
# '.' meaning in the current dir.
from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    # Importing the func module and letting sqlalchemy do it for us. In terms of setting a date. Each note created has a date set. 
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # Associate diff information with diff users / foreign key 
    # User.id coming from user class. In database it is lowercase
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# To create models for other objects. Use the name of the object then parentheses. 
class User(db.Model, UserMixin):
    # Define a schemea or layout
    # For all of our object we need a primary key / unique identifier that represents our object/no other object similar id.
    id = db.Column(db.Integer, primary_key=True)
    # Number inside string is the max characters of email. For "unique" is for no 2 users can have same email 
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # Want all users to find their notes. 
    notes = db.relationship('Note')


# Done with models now we need database creation. In init.py 
