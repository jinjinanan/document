#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#元类
# class ListMetaclass(type):
# 	"""docstring for ListMetaclass"""
# 	def __new__(cls, name,bases,attrs): #1当前准备创建的类的对象，2累的名字，3累积成的父类集合，4类的方法集合
# 		attrs['add'] = lambda self, value:self.append(value)
# 		return type.__new__(cls, name, bases, attrs)

		
# class MyList(list,metaclass = ListMetaclass):
# 	"""docstring for MyList"""
# 	pass

# L = MyList()
# L.add(1)
# L.add(2)
# L.add(3)
# L.add('END')
# print(L)


class  Field(object):
	"""docstring for  Field"""
	def __init__(self, name, colun_type):
		self.name = name
		self.colun_type = colun_type

	def __str__(self):
		return '%s:%s' % (self.__class__.__name__, self.name)
		
class StringField(Field):
	"""docstring for StringField"""
	def __init__(self, name):
		super(StringField,self).__init__(name,'varchar(100)')

class IntegerField(Field):
	"""docstring for IntegerField"""
	def __init__(self, name):
		super(IntegerField, self).__init__(name,'bigint')
		


# class User(Model):
#     # 定义类的属性到列的映射：
#     id = IntegerField('id')
#     name = StringField('username')
#     email = StringField('email')
#     password = StringField('password')

# # 创建一个实例：
# u = User(id=12345, name='Michael', email='test@orm.org', password='my-pwd')
# # 保存到数据库：
# u.save()

#	继承object的新类才有__new__
#__new__：创建对象时调用，返回当前对象的一个实例,有一个cls参数，此参数实例化时候有Python自动提供
# __init__：创建完对象后调用，对当前对象的实例的一些初始化，无返回值。有一个参数，是__new__
# 返回的实例

class ModelMetaclass(type):
	"""docstring for ModelMetaclass"""
	def __new__(cls, name, bases, attrs):
		if name =='Model':
			return type.__new__(cls, name,bases,attrs)
		print('Found model:%s' % name)
		mappings = dict()
		for k, v in attrs.items():
			if isinstance(v, Field):
				print('Found mapping:%s ===> %s'%(k,v))
				mappings[k] = v
		for k in mappings.keys():
			attrs.pop(k)
		attrs['__mappings__'] = mappings #跑存属性和列的映射关系
		attrs['__table__'] = name # 假设表名和类名一致
		return type.__new__(cls, name, bases, attrs)



	"""- super用法：在子类中调用父类的方法。
       - super其实和父类没有实质性的关系 MRO（Method Resolution Order）代表类继承的顺序
       - 原理：
       	def super(cls,inst)   cls 代表类，inst 代表实例
       		mro = inst.__class__.mro()			获取inst的MRO列表
    		return mro[mro.index(cls) + 1]		查找cls当前MRO列表中的index，并返回下一个类

    		http://python.jobbole.com/86787/
	"""
class Model(dict,metaclass = ModelMetaclass):
	def __init__(self, **kw):
		super(Model, self).__init__(**kw)
	def __getter__(self,key):
		try:
			return self[key]
		except Exception as e:
			raise AttributeError(r" 'Model' object has no attribute '%s' "%key)
	def __setattr__(self,key,value):
			self[key] = value
		

	def save(self):
		fields = []
		params = []
		args = []
		for k, v in self.__mappings__.items():
			fields.append(v.name)
			params.append('?')
			args.append(getattr(self,k,None))
		sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
		print('SQL:%s' % sql)
		print('ARGS: %s' % str(args))
		

#测试
class User(Model):
    # 定义类的属性到列的映射：
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')
u = User(id=12345, name='Michael', email='test@orm.org', password='my-pwd')
u.save()
		
