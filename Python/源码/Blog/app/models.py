#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import db
from flask_login import UserMixin,AnonymousUserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer # 生成令牌使用itsdangerous包
from flask import current_app,request
from datetime import datetime
import hashlib
from markdown import markdown
import bleach



from werkzeug.security import generate_password_hash,check_password_hash

#Flask-Login 的回调函数，使用指定的标识符加载用户
#@login_manager.user_loader()   表示调用此方法需要传入一个参数
#@login_manager.user_loader     表示装饰器，把load_user(user_id)函数传入装饰器
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Follow(db.Model):
    __tablename__ = 'Follow'
    follower_id = db.Column(db.Integer,db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer,db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(30),index = True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    email = db.Column(db.String(25), unique=True, index=True)
    confirmed = db.Column(db.Boolean,default=False)
    reset_email = db.Column(db.String(25))

    name = db.Column(db.String(64))     #真实姓名
    location = db.Column(db.String(64)) #地址
    about_me = db.Column(db.TEXT())     #自我介绍
    #  default 参数可以接受函数作为默认值，所以每次需要生成默认值时
    member_since = db.Column(db.DateTime(),default=datetime.utcnow)   #注册日期
    last_seen = db.Column(db.DateTime(),default=datetime.utcnow)      #最后访问日期

    avatar_hash = db.Column(db.String(32))

    posts = db.relationship('Post',backref='author',lazy='dynamic')


    #dynamic 不会返回查询结果，而是返回查询对象
    #粉丝
    followed = db.relationship('Follow',foreign_keys = [Follow.follower_id],
                               backref = db.backref('follower',lazy = 'joined'),
                               lazy = 'dynamic',cascade='all, delete-orphan')

    #我关注的人
    followers = db.relationship('Follow',foreign_keys = [Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy = 'dynamic',cascade='all, delete-orphan')

    comments = db.relationship('Comment',backref = 'author',lazy = 'dynamic')



    def __init__(self,**kw):
        super(User,self).__init__(**kw)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions = 0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default_role = True).first()
        if self.email is None or self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        self.follow(self)

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

    def can(self,permissions):
        """请求和赋予角色这两种权限之间进行位与操作"""
        return self.role is not None and (self.role.permissions & permissions) == permissions


    def is_administrator(self):
        return self.can(Permission.ADMINTSTER)

    # 每次收到用户的请求时都要调用 ping() 方法
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravator(self,size = 100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'\
            .format(url = url,hash = hash,size = size,default = default,rating = rating)

    def follow(self,user):
        '''查询'''
        if not self.is_following(user):
            f = Follow(follower = self,followed = user)
            db.session.add(f)

    def unfollow(self,user):
        f = self.followed.filter_by(followed_id = user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self,user):
        '''这个人是否是我粉丝'''
        return self.followed.filter_by(followed_id = user.id).first() is not None

    def is_followed_by(self,user):
        ''' 我是否关注了这个人'''
        return self.followers.filter_by(follower_id = user.id).first() is not None

    @property
    def followed_posts(self):
        return Post.query.join(Follow,Follow.followed_id == Post.author_id)\
            .filter(Follow.follower_id == self.id)


        # 生成虚拟数据

    @staticmethod
    def generate_fake(count=1000):
        # 这个异常的处理方式是，在继续操作之前回滚会话。
        # 在循环中生成 重复内容时不会把用户写入数据库，因此生成的虚拟用户总数可能会比预期少
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py
        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     confirmed=True,
                     name=forgery_py.name.full_name(),
                     location=forgery_py.address.city(),
                     about_me=forgery_py.lorem_ipsum.sentence(),
                     member_since=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @staticmethod
    def add_self_follows():
        for user in User.query.all():
            if not user.is_following(user):
                user.follow(user)
                db.session.add(user)
                db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    """程序不用先检查用户是否登录，就能自由调用 current_user.can() 和 current_user.is_administrator()"""
    def can(self,permissions):
        return False

    def is_administratior(self):
        return False

    # login_manager.anonymous_user =
    def __repr__(self):
        return '<User %r>' % self.username

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),unique=True)
    # 只有一个角色的 default 字段要设为 True，其他都设为 False。
    # 用户注册时，其角色会被设为默认角色。
    default_role = db.Column(db.Boolean,default=False,index=True)
    # 各操作都对应一个位位置，能执行某项操作的角色，其位会被设为 1
    permissions = db.Column(db.Integer)
    users = db.relationship('User',backref='role',lazy = 'dynamic')

    # 匿名          0b00000000(0x00)            未登录的用户。在程序中只有阅读权限
    # 用户          0b00000111(0x07)            具有发布文章、发表评论和关注其他用户的权限。这是新用户的默认角色
    # 协管员         0b00001111(0x0f)            增加审查不当评论的权限
    # 管理员         0b11111111(0xff)            具有所有权限，包括修改其他用户所属角色的权限
    @staticmethod
    def insert_roles():
        roles = {
            'User':(Permission.FOLLOW |
                    Permission.COMMENT |
                    Permission.WRITE_ARTICLES,True),
            'Moderator':(Permission.FOLLOW |
                         Permission.COMMENT |
                         Permission.WRITE_ARTICLES |
                         Permission.MODERATE_COMMENTS,False),
            'Administrator':(0xff,False)
        }
        for r in roles:
            # import pdb
            # pdb.set_trace()
            role = Role.query.filter_by(name = r).first()
            if role is None:
                role = Role(name = r)
            role.permissions = roles[r][0]
            role.default_role = roles[r][1]
            db.session.add(role)
        db.session.commit()


class Permission:
    FOLLOW = 0x01                   #0b00000001(0x01) 关注用户
    COMMENT = 0x02                  #0b00000010(0x02) 在他人撰写的文章中发布评论
    WRITE_ARTICLES = 0x04           #0b00000100(0x04) 写原创文章
    MODERATE_COMMENTS = 0x08        #0b00001000(0x08) 查处他人发表的不当评论
    ADMINTSTER = 0x80               #0b10000000(0x80) 管理网站


class Post(db.Model):
    __tablename__ = 'Post'
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    body_html = db.Column(db.Text)

    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    @staticmethod
    def generate_fake(count = 100):
        from random import seed,randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0,user_count - 1)).first()
            p = Post(body = forgery_py.lorem_ipsum.sentences(randint(1,5)),
                     timestamp = forgery_py.date.date(True),
                     author = u)
            db.session.add(p)
            db.session.commit()

    @staticmethod
    def on_changed_body(target,value,oldvalue,initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                             'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                             'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.\
            linkify(bleach.clean(markdown(value,output_format='html'),
                                 tags=allowed_tags,strip=True))



class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.Text)
    body.html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('Post.id'))


    @staticmethod
    def on_changed_body(target,value,oldvalue,initiator):
        allowed_tags = ['a','abbr','acronym','b','code','em','i','strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value,output_format = 'html'),
            tags=allowed_tags,strip=True
        ))


# on_changed_body 函数注册在 body 字段上，是 SQLAlchemy“set”事件的监听程序，
# 这意 味着只要这个类实例的 body 字段设了新值，函数就会自动被调用
db.event.listen(Post.body,'set',Post.on_changed_body)

db.event.listen(Comment.body,'set',Comment.on_changed_body)








