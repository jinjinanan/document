#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#一旦决定使用异步，则系统每一层都必须是异步

import asyncio
import aiomysql

@asyncio.coroutine
def create_pool(loop,**kw)
    logging.info('create database connection pool...')
    global __pool
    __pool = yield from aiomysql.create_pool(
        host = kw.get('host',)
    )