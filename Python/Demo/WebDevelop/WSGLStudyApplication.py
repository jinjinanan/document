#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Web Server Gateway Interface

def application(environ,start_response):
    start_response('200 OK',[('Content-Type','text/html')])
    return [b'<h1>Hello, web!</h1>']