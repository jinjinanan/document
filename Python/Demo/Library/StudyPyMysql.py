#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#http://www.cnblogs.com/wt11/p/6141225.html
import pymysql
from pymysql import OperationalError

#创建连接
def connect():
    try:
        conn = pymysql.connect(host='120.25.247.186',
                               port=3306,
                               user='clbMacBookPro',
                               password='clbMacBookPro',
                               database='awesome',
                               charset='utf8'  # 只需要utf8
                               )
    except OperationalError as e :
        print('连接数据库错误')
        return None

    # 创建游标
    cursor = conn.cursor()
    return cursor,conn

def insert(cur,word,chinese,aPhoneticSymbol = '',note = ''):
    sql = ' INSERT INTO wordList (word,chinese,aPhoneticSymbol,note) ' \
          'VALUES("%s","%s","%s","%s");' % (word,chinese,aPhoneticSymbol,note)
    effect_row = cur.execute(
        sql)
    print('执行sql语句' + sql, cur.lastrowid)
    return cur

def query(cur):
    cur.execute('SELECT * FROM wordList')
    row = cur.fetchall()
    print(row)
    return cur

def delect(cur,word):
    sql = 'DELETE FROM wordList WHERE word = \'%s\'; ' % (word)
    print('执行删除语句：'+ sql)
    effect_row = cur.execute(sql)
    print('DELECT' + str(effect_row) )
    return cur


def main():
    cursor,conn = connect()
    if cursor :
        print('进入')
        insert(cursor,'once','一旦；曾经','wʌns','')
        query(cursor)
        delect(cursor,'once')
    # 提交，不然无法保存新建或者修改的数据
    conn.commit()

    # 关闭游标
    cursor.close()

    # 关闭连接
    conn.close()

main()




