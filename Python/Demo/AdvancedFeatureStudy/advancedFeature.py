#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#切片
L = ['Michael','sarah','Tracy','Bob','Jack']
print(L[0:3])

#返回函数
#	打印结果
# >>> f = lazy_sum(1,3,4,5,8)
# >>> f
# <function sum at 0x102dbbc80>		打印的是一个结果
#
# >>> f()
# 21
def lazy_sum(*args):
	def sum():
		ax = 0
		for n in args:
			ax = ax + n
		return ax
	return sum
# 	函数lazy_sum中定义了函数sum，并且，内部函数sum可以引用外部函数lazy_sum的参数和局部变量，
# 当lazy_sum返回函数sum时，相关参数和变量都保存在返回的函数中，这种称为“闭包（Closure）”

# 返回函数不要引用任何循环变量，或者后续会发生变化的变量。
# 防止引用的外部变量变化
def count():
    def f(j):
        def g():
            return j*j
        return g
    fs = []
    for i in range(1, 4):
        fs.append(f(i)) # f(i)立刻被执行，因此i的当前值被传入f()
    return fs


#装饰器
#	打印结果
#>>> now()
#call now():
#2017-4-26
def log(func):
	def wrapper(*args, **kw):
		print('call %s():' % func.__name__)
		return func(*args, **kw)
	return wrapper

@log
def now():
	print('2017-4-26')

# 带参数的装饰器
def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

@log('execute')
def now():
	print(2017-4-26)


# 偏函数（Partial function）
# 正常的函数和变量名是公开的（public），可以被直接引用，比如：abc，x123，PI
# _xxx和__xxx这样的函数或变量就是非公开的（private）





#动态给类绑定属性
#>>> s = sun()
#>>> s.name = 'Michael'
#>>> print(s.name)
#Michael
class sun(object):
    pass



#使用__slots__
class Student(object):
    __slots__ = ('name','age') #使用
