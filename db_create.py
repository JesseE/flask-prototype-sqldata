from app import db
from models import BlogPost

#create database db tables
db.create_all()
#insert 
db.session.add(BlogPost("GOOD","I\'m good."))
db.session.add(BlogPost("Well","I\'m well."))

#commit the changes
db.session.commit()