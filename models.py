from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from extensions import db

class Student(db.Model):
   __tablename__ = "students"
    
   id = db.Column(db.Integer, primary_key = True) 
   name = db.Column(db.String(100),nullable = False)
   email = db.Column(db.String(150),nullable =False)
   standard = db.Column(db.Integer,nullable = False)
   devision = db.Column(db.Integer,nullable = False)
 
   def __repr__(self):
        return f"<User {self.name}>"

