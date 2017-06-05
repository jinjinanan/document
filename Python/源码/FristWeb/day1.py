#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask

from flask import app
from flask import current_app
from flask import request
from flask import make_response
from flask import redirect  #重定向
from flask import abort     #用于处理错误
from flask.ext.script import Manager

app = Flask(__name__)  # python的 __name__。  Flask 用这个参数决定程序的根目录，以便稍后能够找到相对于程 序根目录的资源文件位置。
manager = Manager(app)

# 程序实例需要知道对每个 URL 请求运行哪些代码，所以保存了一个 URL 到 Python 函数的映射关系。处理 URL 和函数之间关系的程序称为路由
# 惯常用法是使用修饰器把函数注册为事件的处理程序。
@app.route('/')
def index():  # view function
    return '<h1>Hello World!</h1>'

@app.route('/usr/<name>')  # 尖括号表示动态的部分
def usr(name):
    return '<h1>Hello, %s!</h1>' % name


#---------Flask---------上下文
#全局上下文

#请求上下文
@app.route('/user_agent')
def testUser_agent():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your brower is %s</p>' % user_agent


#---------Flask---------响应
#response
@app.route('/badRequest')
def testBadRequest():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer','42')
    return response

#重定向
@app.route('/testRediret')
def testRediret():
    return redirect('http://www.baidu.com')

#abort 用于处理错误
# @app.route('/usr/<id>')
# def testAbort(id):
#     usr = load_user(id)
#     if not usr:
#         abort(404)
#     return '<h1>hello %s</h1>' % usr.name


if __name__ == '__main__':
    # app.run(debug=True)
    # print(app.url_map)
    manager.run()

