#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#特点：在执行函数A的时候，可以随时中断去执行函数B
#协程优势： 1.没有切换线程，避免了线程切换的开销 2.避免了多线程的锁的机制

def consummer():
    r = ''
    while True:
        n = yield r
        if not n :
            return
        print('[CONSUMER] Consuming %s...' %n)
        r = '200 OK'


def product(c):
    c.send(None)     #启动生成器；
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' %n)
        r = c.send(n)       #
        print('[PRODUCER] Consumer return: %s' %r)
    c.close()

c = consummer()
product(c)