#/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform

class Component(object):
	def report(self):
		pass

	def sign(self):
		pass

class ConcreteComponent(Component):
	
	def  report(self):
		print('我是一个报告')

	def sign(self):
		print('老大签字')


class Decorator(Component):
	_isDecorated = None

	def __init__(self,isDecorated):
		self._isDecorated = isDecorated

	def report(self):
		self._isDecorated.report()

	def sign(self):
		self._isDecorated.sign()

class DecoratorComponentA(Decorator):
	# def __init__(self,isDecorated):
	# 	super().__init__(isDecorated)

	def decorateFunA(self):
		print('这是一个修饰器A')

	def report(self):
		self.decorateFunA()
		# super(DecoratorComponentA,self).report()		#python2.7
		super().report()								#python3 以上

	def sign(self):
		super.report()

class DecoratorComponentB(Decorator):
	def decorateFunB(self):
		print('这是一个装饰器B')

	def report(self):
		self.decorateFunB()
		super(DecoratorComponentB,self).report()

	def sign():
		super.report()

if __name__ == '__main__':
	print(platform.python_version())
	c = ConcreteComponent()
	c = DecoratorComponentA(c)
	c = DecoratorComponentB(c)
	c.report()

