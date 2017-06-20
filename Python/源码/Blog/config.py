#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # 字典可用来存储框架、扩展和程序本身的配置变量
    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.qq.com'                       #电子邮件服务器的主机名或 IP 地址
    MAIL_PORT = 25                                      #电子邮件服务器的端口
    MAIL_USE_TLS = True                                 #启用传输层安全(Transport Layer Security，TLS)协议
    # MAIL_USE_SSL                                        #启用安全套接层(Secure Sockets Layer，SSL)协议
    MAIL_USERNAME = '798618564@qq.com' #os.environ.get('MAIL_USERNAME')     #邮件账户的用户名
    MAIL_PASSWORD = 'xmllnbotgozlbfeb'#os.environ.get('MAIL_PASSWORD')     #邮件账户的密码
    FLASKY_MAIL_SUBJECT_PREFIX = '[clb]'
    FLASKY_MAIL_SENDER = '798618564@qq.com'

    @staticmethod
    def init_app(app):      #可以执行对当前 环境的配置初始化。现在，基类 Config 中的 init_app() 方法为空
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI =  'mysql+pymysql://clbMacBookPro:clbMacBookPro@120.25.247.186:3306/awesome?charset=utf8'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI =  'mysql+pymysql://clbMacBookPro:clbMacBookPro@120.25.247.186:3306/awesome?charset=utf8'


class ProductionConfig(Config):
    pass

config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,

    'default':DevelopmentConfig
}

