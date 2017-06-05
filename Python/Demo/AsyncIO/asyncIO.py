#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import threading
# @asyncio.coroutine #把一个generator标记为coroutine类型,然后，我们就把这个coroutine扔到EventLoop中执行。
# def hello():
#     print('hello world!')
#     # 异步调用asyncio.sleep(1):
#     r = yield from asyncio.sleep(1)
#     print('hello again')
#
# # 获取EventLoop：
# loop = asyncio.get_event_loop()
# #执行coroutine
# loop.run_until_complete(hello())
# loop.close()

#Python3.5  把@asyncio.coroutine替换为async；
#           把yield from替换为await。

@asyncio.coroutine
def hello1():
    print('hello world (%s)' % threading.currentThread() )
    yield from asyncio.sleep(5)
    print('hello again %s',threading.currentThread())

loop = asyncio.get_event_loop()
task = [hello1(),hello1()]
loop.run_until_complete(asyncio.wait(task))
loop.close()
