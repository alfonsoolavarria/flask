from app import db
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model,UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    password = db.Column(db.String(300))
    email = db.Column(db.String(100),unique=True, nullable=False)
    picture = db.Column(db.String(100),nullable=True)
    is_active = db.Column(db.Boolean())
    is_anonymous = db.Column(db.Boolean())
    is_authenticated = db.Column(db.Boolean())

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)



    def __init__(self, name, password, email, picture, status, is_anonymous,is_authenticated):
        self.name = name
        self.email = email
        self.picture = picture
        self.status = status
        self.is_anonymous = is_anonymous
        self.is_authenticated = is_authenticated
        self.password = generate_password_hash(password)


    def __repr__(self):
        return '%s/%s/%s' % (self.id, self.name, self.email)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

class Publication(db.Model):
    __tablename__ = "publication"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(255))
    prioridad = db.Column(db.String(255))
    status = db.Column(db.Boolean())
    created = db.Column(db.DateTime(255))
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'),nullable=False )

    def __init__(self, title, description, prioridad,status,created,user_id):
        self.title = title
        self.description = description
        self.prioridad = prioridad
        self.status = status
        self.created = created
        self.user_id = user_id

    def __repr__(self):
        return '%s/%s' % (self.id, self.title)
