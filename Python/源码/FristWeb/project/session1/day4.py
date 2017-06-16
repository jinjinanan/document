#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# http://www.jianshu.com/p/9771b0a3e589
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, create_engine,Integer,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask

from flask import Flask
from flask import render_template, session, redirect, url_for,flash


from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from wtforms import validators
from flask.ext.bootstrap import Bootstrap


app = Flask(__name__)
Base = declarative_base()
# db = SQLAlchemy(app)

engine = create_engine('mysql+pymysql://clbMacBookPro:clbMacBookPro@120.25.247.186:3306/awesome?charset=utf8')
#创建DBSession类型
DBSession = sessionmaker(bind=engine)
sessiondb = DBSession()

bootscript = Bootstrap(app)
app.config['SECRET_KEY'] = 'clbTest'

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    username = Column(String(30), unique=True)
    role_id = Column(Integer,ForeignKey('roles.id'))


    # def __init__(self,username,role):
    #     self.username = username
    #     self.id = id

    def __repr__(self):
        return '<User %r>'% self.username

    def save(self):
        sessiondb.add(self)
        sessiondb.commit()

class role(Base):
    __tablename__ = 'roles'
    id = Column(Integer,primary_key=True)
    name = Column(String(30))
    users = relationship('User',backref = 'role',lazy ='dynamic')

    def __init__(self,name):

        self.name = name

    def __repr__(self):
        return '<name %r>'% self.name

    def save(self):
        sessiondb.add(self)
        sessiondb.commit()

def testQuery(condation):
    r = role;
    roles = sessiondb.query(r).filter(r.name == condation).all()
    print(roles)
    if len(roles) > 0:
        return roles[0]
    return None

#删除，插入，更新，只有提交会话才会更新数据库
def testAdd():
    r = role('User')
    u = User(username='john', role=r)
    sessiondb.add(u)
    sessiondb.commit()
    sessiondb.close()


def testDelte(c):
    sessiondb.delete(c)

def testUpdate():
    sessiondb.dirty
    sessiondb.commit()
    sessiondb.close()

def testDatabase():
    # r = testQuery()
    # r.name = 'Administrator'
    # testUpdate()
    testQuery(condation='Administrator')




class NameForm(Form):
    name = StringField('What is your name?',validators=[validators.required()])
    submit = SubmitField('submit')

@app.route('/',methods=['GET','POST'])
def testForm():
    form = NameForm()
    if form.validate_on_submit():
        u = User
        user = sessiondb.query(u).filter_by(username = form.name.data).first()
        if user is None:
            user = User(username = form.name.data,role_id = 1 )
            sessiondb.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('testForm'))        # url_for 重定向的是方法名
    return render_template('day3/day4From.html',
                           form = form,
                           name=session.get('name'),
                           known = session.get('known',False))

if __name__ == '__main__':
    app.run()








