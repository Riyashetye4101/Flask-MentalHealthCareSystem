from enum import unique
from mental import db,login_manager
from datetime import datetime,date
from mental import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))


class Customer(db.Model,UserMixin):
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(length=200),nullable=False,unique=True)
    name=db.Column(db.String(length=200),nullable=False)
    email=db.Column(db.String(length=100),nullable=False,unique=True)
    pswd=db.Column(db.String(length=50),nullable=False)
    mobile=db.Column(db.String(length=10),nullable=False,unique=True)
    age=db.Column(db.String(length=3),nullable=False)
    child=db.relationship('Test',backref='parent',lazy='dynamic')
    
    def __repr__(self):
        return f'User:{self.name}'

    @property
    def password(self):
        return self.password
    @password.setter
    def password(self,plain_text_password):
        self.pswd=bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.pswd, attempted_password)

class Test(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    tname=db.Column(db.String(length=100),nullable=False)
    result=db.Column(db.String(length=10),nullable=False)
    date=db.Column(db.DateTime(),nullable=True)
    activity=db.Column(db.String(1000),nullable=True)
    end=db.Column(db.DateTime(),nullable=True)
    level=db.Column(db.String(length=10),nullable=True)
    senddate=db.Column(db.Date(),nullable=True)
    parent_id=db.Column(db.Integer(),db.ForeignKey('customer.id'))
    

    def __repr__(self):
        return f'test:{self.tname}'

