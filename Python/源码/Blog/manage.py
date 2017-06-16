#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from app import create_app,db
from app.models import User,Role
from flask_script import Manager,Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app('default')
app.debug = True            # 你启用了调试支持，服务器会在代码修改后自动重新载入，并在发生 错误时提供一个相当有用的调试器
manager = Manager(app)

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)


manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()