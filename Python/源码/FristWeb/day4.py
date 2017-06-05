#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://clbMacBookPro:clbMacBookPro@120.25.247.186:3306/awesome'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

class word(db.Model):
    __tablename__ = 'wordList'
    # 表的结构
    word = db.Column(db.String(20), primary_key=True)
    chinese = db.Column(db.String(80))
    aPhoneticSymbol = db.Column(db.String(80))
    note = db.Column(db.String(100))

    def __repr__(self):
        return 'word %r' %self.word