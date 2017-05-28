#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#模块导入
import socket
import threading

#全局变量
HOST = '127.0.0.1'
PORT = 9998
NUMBER = 0,
ADDR = (HOST,PORT)

#类定义


#函数定义
def createS(addr = ADDR,number = NUMBER):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(ADDR)
    s.listen(number)
    return s

    #处理请求事物
def tckHandLink(sock,addr):
    print('Accept new connection from %s:%s...' % addr)
    # sock.send('欢迎使用clb的wordList！'.encode('utf-8'))
    while True:
        data = sock.recv(2048)  # !!!
        if not data or data.decode('utf-8') == 'exit':
            print('发送了空的数据')
            break
        else:
            print('已经接收到数据：%s', data.decode('utf-8'))
            sock.send(('收到数据%s' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('连接关闭')


#主程序
def main():
    s = createS(number = 5)
    #循环接受新连接
    while True:
        sock, addr = s.accept()     #accept()是阻塞的，这意味着执行将被暂 ，直到一个连接到达。非阻塞模式？？？操作系统教材或文档
        print(sock,addr)
        t = threading.Thread(target=tckHandLink,args=(sock,addr)) #!!!
        t.start()



main()