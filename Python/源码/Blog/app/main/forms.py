#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import required

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[required()])
    submit = SubmitField('Submit')