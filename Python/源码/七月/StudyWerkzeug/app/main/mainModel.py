from .. import db

class NavModel(object):
    def __init__(self,name,element_id,url):
        self.name = name
        self.element_id = element_id
        self.url = url

class indexModel(object):
    def __init__(self,indicators,imgSrc):
        self.indicators = indicators
        self.imgSrc = imgSrc

class userModel(db.Model):
    __tablename__ = 'user'
    name = db.Column(db.CHAR(255))
    password = db.Column(db.CHAR(255))
    email = db.Column(db.CHAR(255))
    id = db.Column(db.Integer,primary_key=True)

    def __repr__(self):
        return '<User %r>'% self.username






