
from werkzeug.security import check_password_hash,generate_password_hash
from .. import db


class userModel(db.Model):
    __tablename__ = 'user'
    name = db.Column(db.CHAR(255))
    password_hash = db.Column(db.CHAR(255))
    email = db.Column(db.CHAR(255))
    id = db.Column(db.Integer,primary_key=True)

    @property
    def password(self):
        raise (u'该属性不可访问')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)



    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<User %r>'% self.username

class NavModel(object):
    def __init__(self,name,element_id,url):
        self.name = name
        self.element_id = element_id
        self.url = url

class indexModel(object):
    def __init__(self,indicators,imgSrc):
        self.indicators = indicators
        self.imgSrc = imgSrc




