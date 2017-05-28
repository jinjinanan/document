#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#模块导入
import socket

#全局变量
HOST = '127.0.0.1'
PORT = 9998
NUMBER = 0,
ADDR = (HOST,PORT)

#类定义


#函数定义
def createS(addr=ADDR):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    return s

    #添加数据
def addWord(sock,word = '',chinese = '',aPhoneticSymbol = '',note = ''):
    data = [word,chinese,aPhoneticSymbol,note]
    for con in data :
        sock.send(con.encode('utf-8'))
    print(sock.recv(1024).decode('utf-8'))



#主程序
def main():
    sock = createS()
    addWord(sock,word='invocation',chinese='调用',aPhoneticSymbol='haha',note='我')
    sock.close()

main()