#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#著名的Python ORM 1.SQLAlchemy, 2.SQLObject


from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


#创建对象的基类
Base = declarative_base()

#定义word对象
class Word(Base):
    #表的名字
    __tablename__ = 'wordList'

    #表的结构
    word = Column(String(20), primary_key=True)
    chinese = Column(String(80))
    aPhoneticSymbol = Column(String(80))
    note = Column(String(100))

#初始化数据库连接
# '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
engine = create_engine('mysql+pymysql://clbMacBookPro:clbMacBookPro@120.25.247.186:3306/awesome?charset=utf8',)
#创建DBSession类型
DBSession = sessionmaker(bind=engine)

session = DBSession()

def insert(word = '',chinese = '',aPhoneticSymbol = '',note = ''):
    try:
         #注意，mysql是utf-8,而这里是unicode所以要转码
        new_word = Word(word=word, chinese=chinese.encode(), aPhoneticSymbol=aPhoneticSymbol.encode(), note=note.encode())
        session.add(new_word)
    except UnicodeEncodeError as e:
        print('编码错误')
    finally:
        session.commit()
        # session.close()

def query(word = ''):
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    words = session.query(Word).filter(Word.word == word).all()

    print('type:',type(words))
    print('num:',len(words))
    for word in words:
        print('word:', word.word)
        # 1.b'xxx'表示bytes类型的数据.
        #encode: 将其他编码的字符串转换成unicode编码 和 decode:将unicode编码转换成其他编码的字符串
        # 2.python3 目前都是unicode 编码，因此没有decode方法
        #！！！！！！！！在create_engine()的连接后加上编码格式，防止出现中文乱码！！！！！！！！！！！！
        print('chinese:',word.chinese)
    # session.close()
    if len(words) > 0:
        return words[0]

def update(instance,word = '',chinese = '',aPhoneticSymbol = '',note = ''):
    if len(word) > 0:
        instance.word = word
    if len(chinese) > 0:
        instance.chinese = chinese
    if len(aPhoneticSymbol) > 0:
        instance.aPhoneticSymbol = aPhoneticSymbol
    if len(note) > 0:
        instance.note = note
    print(instance.word,instance.chinese)
    print(session.dirty)
    session.commit()
    # session.close()

def delete(instance):
    session.delete(instance)
    session.commit()

def main():
    # insert(word='once',chinese='一次')
    word = query(word='test')
    # if word:
    #     delete(word)
    #     update(word,chinese='测试；检查')
    session.close()

main();



