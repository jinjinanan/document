#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#http://www.cnblogs.com/wt11/p/6141225.html
import pymysql

#创建连接
conn = pymysql.connect(host = '120.25.247.186',
                       port= 3306,
                       user = 'clbMacBookPro',
                       passwd = 'clbMacBookPro',
                       db = 'awesome',
                       charset = 'utf-8'
                       )
#创建游标
cursor = conn.cursor()

#执行SQL 并返回影像数据
# effect_row = cursor.execute('SELECT * FROM wordList')
effect_row = cursor.execute('INSERT INTO wordList VALUES(once,一旦；曾经，wʌns，)')

#提交，不然无法保存新建或者修改的数据
conn.commit()

#关闭游标
cursor.close()

#关闭连接
conn.close()

