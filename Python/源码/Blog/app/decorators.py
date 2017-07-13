#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission

def permission_required(permission):
    def decorator(f):
        @wraps(f)   #它能保留原有函数的名称和docstring 因为返回的那个wrapper()函数名字就是'wrapper'，所以，需要把原始函数的__name__等属性复制到wrapper()函数中，否则，有些依赖函数签名的代码执行就会出错。
        def decorated_function(*args,**kw):
            if not current_user.can(permission):
                abort(403)
            return f(*args,**kw)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMINTSTER)(f)