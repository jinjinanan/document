#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from  flask_pagedown.fields import PageDownField
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import required,Length

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[required()])
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    name = StringField('Real name',validators=[Length(0,64)])
    location = StringField('Location',validators=[Length(0.4)])
    about_me = TextAreaField('About Me')
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    body = PageDownField("what's on your mind?",validators=[required()])
    submit = SubmitField('Submit')

