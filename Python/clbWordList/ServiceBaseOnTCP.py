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
    """
    address already in use
    这个是由于你的服务端仍然存在四次挥手的time_wait状态在占用地址
    （如果不懂，请深入研究1.tcp三次握手，四次挥手 2.syn洪水攻击 3.服务器高并发情况下会有大量的time_wait状态的优化方法）。
    """
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

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