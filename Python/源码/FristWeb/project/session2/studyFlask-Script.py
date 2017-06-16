#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_script import Manager,Command,Option

app = Flask(__name__)
manager = Manager(app)

# 创建并且加入命令有三中方法：
#       创建Command子类
#       使用 @command 修饰符
#       使用 @option 修饰符              适用于更精细的命令行控制：

#       1
@manager.command
def hello(name):
    print('hello,%s 这是一个通过@command装饰器添加的命令' % name)

#       2
class hi(Command):
    # 短参数
    option_list = (
        Option('--name', '-n', dest='name'),
    )

    def run(self,name):          #必需是这个函数
        print('hi，%s 这是一个通过创建Command子类，添加的命令' % name)
manager.add_command('hi',hi())

#       3
@manager.option('-n','--name',help='Your name')
@manager.option('-u','--url',help='url')
def hiOption(name,url):
    print('hello '+name)









if __name__ == '__main__':
    manager.run()