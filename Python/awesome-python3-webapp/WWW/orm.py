#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#一旦决定使用异步，则系统每一层都必须是异步

import asyncio
import aiomysql
import pymysql
import  logging

#Python Database API Specification
#https://www.python.org/dev/peps/pep-0249/

#创建一个全局的连接池
@asyncio.coroutine
def create_pool(loop,**kw):
    logging.info('create database connection pool...')
    global __pool   #全局变量
    __pool = yield from aiomysql.create_pool(
        host = kw.get('host','120.25.247.186'),
        port = kw.get('port',3306),
        user = kw['user'],
        password = kw['password'],

    )