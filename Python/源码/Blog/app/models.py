#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import db
from flask_login import UserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer # 生成令牌使用itsdangerous包
from flask import current_app


from werkzeug.security import generate_password_hash,check_password_hash

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(30),index = True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    email = db.Column(db.String(25), unique=True, index=True)
    confirmed = db.Column(db.Boolean,default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def generate_confirmation_token(self,expiration = 3600):
        # TimedJSONWebSignatureSerializer 生成具有过期时间的JSON Web签名包，expires_in 参数设置令牌的过期时间，单位为秒
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        # dump()方法为指定数据生成一个加密签名，然后再对数据和签名进行序列化，生成令 牌字符串
        return s.dumps({'confirm':self.id})

    def confirm(self,token):
        # import pdb;
        # pdb.set_trace()
        s = Serializer(current_app.config['SECRET_KEY'])
        # 为了解码令牌，序列化对象提供了loads()方法，其唯一的参数是令牌字符串
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True


    def __repr__(self):
        return '<User %r>' % self.username

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),unique=True)
    users = db.relationship('User',backref='role',lazy = 'dynamic')


#Flask-Login 的回调函数，使用指定的标识符加载用户
#@login_manager.user_loader()   表示调用此方法需要传入一个参数
#@login_manager.user_loader     表示装饰器，把load_user(user_id)函数传入装饰器
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




