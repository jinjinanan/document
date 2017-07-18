#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Config(object):
    # http://docs.sqlalchemy.org/en/latest/core/index.html
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'clb'
    UPLOAD_FOLDER = '/static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://clbMacBookPro:clbMacBookPro@120.25.247.186:3306/StudyWerkzeug?charset=utf8'
    DEBUG = True


config = {
    'default': DevelopmentConfig
}
