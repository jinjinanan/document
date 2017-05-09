#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from wsgiref.simple_server import make_server
from WSGLStudyApplication import application

httpd = make_server('', 8000, application)
print('service http on port 8000...')
httpd.serve_forever()