#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging;logging.basicConfig(level=logging.INFO)

import asyncio,os,json,time
from datetime import datetime

from aiohttp import web

def index(request):
    return  web.Response(body=b'<h1>Awesome</h1>',content_type='text/html')

@asyncio.coroutine                  #使用异步IO
def init(loop):                     # loop 为消息循环EventLoop
    app = web.Application(loop = loop)
    app.router.add_route('GET','/',index)
    #http://stackoverflow.com/questions/9708902/in-practice-what-are-the-main-uses-for-the-new-yield-from-syntax-in-python-3
    srv = yield from loop.create_server(app.make_handler(),'127.0.0.1', 9000) # 可以从yield from 拿到返回值
    logging.info('server started at http://127.0.0.1:9000...')
    return srv
loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()