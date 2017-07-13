
from flask import render_template
from . import main
from .mainModel import NavModel
import random

@main.route('/')
def index():
    return render_template('main.html')


@main.route('/JQuery')
def jquery():
    return render_template('JQuery.html')

@main.route('/bootstrap')
def bootstrap():
    v1 = NavModel(name='主页',element_id='zhuye',url='#zhuye')

    return render_template('bootstrap.html',list = [v1])


