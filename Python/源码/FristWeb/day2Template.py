#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime


app = Flask(__name__)
bootscrap = Bootstrap(app)
momnet = Moment(app)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/usr/<name>')        #在模板中使用的 {{ name }} 结构表示一个变量，它是一种特殊的占位符，告诉模板引擎这个位置的值从渲染模板时使用的数据中获取。
def testUser(name):
    return render_template('User.html',name=name,
                           mydict={'key':'我是字典key的值'},
                           mylist=['0','1','2','3','4'],
                           comment = ['aaa','bbb','ccc','ddd']
                           )

@app.route('/testExtends')
def testExtends():
    return render_template('extends.html')

@app.route('/testBootScript/<name>')
def testBootScript(name):
    return render_template('testbootScript.html',
                          name = name,
                           current_time = datetime.utcnow())

@app.errorhandler(404)
def test404(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def test500(e):
    return render_template('500.html'),500

if __name__ == '__main__':
    app.run()
