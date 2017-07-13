#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Config(object):

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'default':DevelopmentConfig
}