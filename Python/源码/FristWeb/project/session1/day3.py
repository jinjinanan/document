#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template, session, redirect, url_for,flash


from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from wtforms import validators
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
bootscrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'

class NameForm(Form):
    name = StringField('What is your name?',validators=[validators.required()])
    submit = SubmitField('submit')

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/testForm/',methods=['GET','POST'])
# def testForm():
#     name = None
#     form = NameForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         print(name)
#         form.name.data = ''
#     return render_template('day3/form.html',
#                            form = form,
#                            name=name)

# @app.route('/testForma',methods=['GET','POST'])
# def testForm():
#     name = None
#     form = NameForm()
#     if form.validate_on_submit():
#         session['name'] = form.name.data
#         return redirect(url_for('testForm'))
#     return render_template('day3/form.html',
#                            form = form,
#                            name=session.get('name'))

@app.route('/testForma',methods=['GET','POST'])
def testForm():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session['name']
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('testForm'))
    return render_template('day3/form.html',
                           form = form,
                           name=session.get('name'))


if __name__ == '__main__':
    app.run()