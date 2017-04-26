#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math			#导入math包

print('请输入一个数字') 
# 在Python解释器下： from abstest import my_abs，如有此行会报错
x = input()
def my_abs(x):
    if x >= 0:
        return x
    else:
        return -x

print(my_abs(float(x)))

#空函数
#pass 占位符
def nop():
	pass

#返回多个参数值
def move(x,y,step,angle=0):
	nx = x + step * math.cos(angle)
	ny = y - step * math.sin(angle)
	return nx, ny

#可变参数 只需在前面加一个 * 号
def calc(*numbers):
	sum = 0
	for n in numbers:
		sum = sum + n * n
	return sum

#关键字参数
# 调用
# 	>>> person('clb',25,city='nanyang')
# 	('name:', 'clb', 'age:', 25, 'other:', {'city': 'nanyang'})
def person(name,age,**kw):
	print('name:',name,'age:',age,'other:',kw)


#必选参数、默认参数、可变参数、关键字参数和命名关键字参数
