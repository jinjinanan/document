
from flask import render_template,url_for,flash
from . import main
from .forms import loginForm,registForm
from .. import db
from flask import redirect
from .mainModel import NavModel,indexModel,userModel



# 一级界面 不需要登陆
@main.route('/')
def index():
    m = indexModel(indicators = ['0','1','2'],imgSrc=['img/nav1.jpg',
                                              'img/nav2.jpg',
                                              'img/nav3.jpg'])
    return render_template('index.html',m = m)

@main.route('/bootstrap')
def bootstrap():
    v1 = NavModel(name='主页',element_id='zhuye',url='#zhuye')
    v2 = NavModel(name='a',element_id='a',url='#a')
    v3 = NavModel(name='b',element_id='b',url='#b')
    v4 = NavModel(name='c',element_id='b',url='#c')

    return render_template('bootstrap.html',list = [v1,v2,v3,v4])

@main.route('/JQuery')
def jquery():
    return render_template('JQuery.html')

@main.route('/login',methods=['GET','POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = userModel.query.filter_by(name = form.username.data).first()
        import pdb
        pdb.set_trace()
        if user is not None and user.verify_password(form.password.data):
            flash('登陆成功')
            return redirect(url_for('main.index'))
    return render_template('login.html',form = form)

@main.route('/regist',methods=['GET','POST'])
def regist():
    form = registForm()
    if form.validate_on_submit():
        m = userModel(email=form.email.data,
                  name=form.username.data,
                    password = form.password.data)
        db.session.add(m)
        db.session.commit()
        flash(u'注册成功', 'message')
        return redirect(url_for('main.index'))
    return render_template('regist.html',form = form)

@main.route('/user')
def user():
    return render_template('main.html')

@main.route('/test')
def test():
    # return render_template('temp.html')
    return redirect(url_for('main.index'))

