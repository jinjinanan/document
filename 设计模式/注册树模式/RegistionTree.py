#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#单例模式
class Singleton(object):  
    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(Singleton, cls)  								#?
            cls._instance = orig.__new__(cls, *args, **kw)  			#?
        return cls._instance  
  
class MyClass(Singleton):  
    a = 1  

 #工厂模式
class LeiFeng(object):
	"""docstring for LeiFeng"""
	def __init__(self):
		super(LeiFeng, self).__init__()


	def buy_rice(self):
		pass
	def sweep(self):
		pass
		
class Student(LeiFeng):
	"""docstring for Student"""
	def __init__(self):
		super(Student, self).__init__()


	def buy_rice(self):
		print('学生帮买米')
	def sweep(self):
		print('学生帮扫地')

class Voluteer(LeiFeng):
	"""docstring for Voluteer"""
	def __init__(self):
		super(Voluteer, self).__init__()

	def buy_rice(self):
		print('志愿者帮买米')
	def sweep(self):
		print('志愿者帮扫地')

class LeiFengFactory(object):
	"""docstring for LeiFengFactory"""
	def __init__(self):
		super(LeiFengFactory, self).__init__()


	def create_LeiFeng(self,type):
		map = {
		'大学生':Student(),
		'志愿者':Voluteer()
		}
		return map[type]
		
#注册树模式
	#	先，单例模式创建唯一对象的过程本身还有一种判断，即判断对象是否存在。存在则返回对象，不存在则创建对象并返
	# 回。 每次创建实例对象都要存在这么一层判断。	
	#	工厂模式更多考虑的是扩展维护的问题。
class Register(object):
	"""docstring for Register"""
	def __init__(self):
		super(Register, self).__init__()
		self.objectDic = {}

	def set(self,name,inst):
		self.objectDic[name] = inst
		print (self.objectDic)
		

	def get(self,name):
		return self.objectDic[name]

	def unset(self,name):
		del self.objectDic[name]
		print(self.objectDic)
		

				


					
		

		




						
		
 		
 		

if __name__ == '__main__':
	a = MyClass()
	b = MyClass()
	print(a == b)
	print(a is b)

	leifeng1 = LeiFengFactory().create_LeiFeng('大学生')
	leifeng2 = LeiFengFactory().create_LeiFeng('志愿者')
	leifeng1.buy_rice()
	leifeng1.sweep()
	leifeng2.buy_rice()
	leifeng2.sweep()
	leifeng2.sweep

	leifeng3 = LeiFengFactory().create_LeiFeng('大学生')
	r = Register()
	r.set(name = 'leifeng',inst = leifeng3)
	c = r.get(name = 'leifeng')
	print(id(c))
	c.buy_rice()
	r.unset(name = 'leifeng')
	print(id(c))

	

			
