from .database import db

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name=db.Column(db.String, nullable=False)
    last_name=db.Column(db.String)
    email_id=db.Column(db.String, unique=True, nullable=False)
    user_name=db.Column(db.String, unique=True, nullable=False)
    password=db.Column(db.String, nullable=False)
    access_token=db.Column(db.String, unique=True)
    role_id=db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

class Role(db.Model):
    __tablename__='role'
    id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    name=db.Column(db.String, nullable=False, unique=True)
    description=db.Column(db.String)
    customers=db.relationship('Customer', backref='role')
    admins=db.relationship('Admin', backref='role')

class Admin(db.Model):
    __tablename__='admin'
    id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    email_id=db.Column(db.String, unique=True, nullable=False)
    user_name=db.Column(db.String, unique=True, nullable=False)
    password=db.Column(db.String, nullable=False)
    access_token=db.Column(db.String, unique=True)
    role_id=db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)


