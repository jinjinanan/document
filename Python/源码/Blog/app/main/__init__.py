#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

main = Blueprint('main',__name__)

from . import views,error       #为了避免循环导入依赖