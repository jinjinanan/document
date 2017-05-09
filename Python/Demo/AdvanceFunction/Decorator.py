#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 装饰器
# def addPrint(temp):
#     def decoorator(*args, **kw):
#         print('by clb')
#         return temp(*args, **kw)
#     return decoorator()
#
# @addPrint
# def now():
#     print('2017-5-1')

#函数作为蚕食并返回函数，已经调用顺序
# def testFunc(*args,**kw):       #传入的参数必须有此两个参数。
#     print('调用testFunc()')
#     print('%s'%args)
#
# def two(func):
#     print('调用了now()')
#     return func('2017')          #在返回函数的时候，也会调用该函数
#
# two(testFunc)
#--------------------------------------------
#
# def add(x,y,f):
#     return f(x) + f(y)
#
# a = add(-6,5,abs)
# print("结果为%s"% a)


#匿名函数
# f = lambda x:x*x
# print(f(5))


