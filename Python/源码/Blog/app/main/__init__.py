#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from ..models import Permission

main = Blueprint('main',__name__)

from . import views,error       #为了避免循环导入依赖

@main.app_context_processor
def inject_permissions():
    return dict(Permission = Permission)