#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket, select, string, sys

def prompt():
    sys.stdout.write('<You>')
    sys.stdout.flush()

if __name__ == '__main__':
    if(len(sys.argv)<3):
        print('Usage : python telnet.py hostname port')
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(2)

    try:

        s.connect((host, port))
    except:
        print('Unable to connect')
        sys.exit()

    print('Connected to remote host. Start sending messages')
    prompt()

    while 1:
        # 监听服务器是否有消息发送过来
        # 检查用户的输入，如果用户输入某条消息，需要发送到服务器
        # 这里有两个I / O事件需要监听：连接到服务器的socket和标准输入，同样我们可以使用
        # select来完成：


        rlist = [sys.stdin,s]
        read_list,write_list,error_list = select.select(rlist,[],[])
        for sock in read_list:
            if sock == s:
                data = sock.recv(4096)
                if not data:
                    print('\nDisconnected from chat server')
                    sys.exit()
                else:
                    sys.stdout.write(data)
                    prompt()
            else:
                msg = sys.stdin.readline()
                s.send(msg)
                prompt()