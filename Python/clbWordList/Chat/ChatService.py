#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#模块导入
import socket,select,threading


# Function to broadcast chat messages to all connected clients
def broadcast_data(sock,message):
    for socket in CONNECTION_LIST:
        if sock != server_socket and socket != sock:
            try:
                socket.send(message)
            except:
                socket.close()
                CONNECTION_LIST.remove(socket)


# Make a script both importable and executable
# 当文件被执行时 __name__ == __main__
# 当文件被导入的时候 __name__ 会输出 __module__
if __name__ == '__main__':

    CONNECTION_LIST = []
    RECV_BUFFER = 4096
    PORT = 9999

    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server_socket.bind(('127.0.0.1',PORT))
    server_socket.listen(10)

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
    print('Chat server started on port '+ str(PORT))

    while 1:
        # Get the list sockets which are ready to be read through select
        # select方法允许你响应不同socket的多个事件以及其它不同事件,
        # 例如你可以让 select 在某个 socket 有数据到达时，或者当某个 socket 可以写数据时，又或者是当某个 socket 发生错误时通知你，
        # 好处是你可以同时响应很多 socket 的多个事件。
        #
        # 当select返回时，说明在read_sockets
        # 上有可读的数据，这里又分为两种情况：
        #



        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

        for sock in read_sockets:


            if socket == server_socket:
                # 如果是主socket（即服务器开始创建的socket，一直处于监听状态）有数据可读，表示有新的连接请求可以接收，此时需要调用
                # accept 函数来接收新的客户端连接，并将其连接信息广播到其它客户端。

                # Handle the case in which there is a new connection recieved through server_socket
                sockfd,addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print('client(%s,%s)connected'% addr)
                broadcast_data(sockfd,'[%s:%s]enterd room \n' % addr)

            #Some incoming message from a client
            else:
                # 如果是其它 sockets（即与客户端已经建立连接的 sockets）有数据可读，那么表示客户端发送消息到服务器端，使用
                # recv 函数读消息，并将消息转发到其它所有连接的客户端。
                try:
                    addr = sock.getpeername
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        #clb getsockname来获取本地地址和端口
                        #clb getpeername获取socket的对方地址
                        broadcast_data(sock,"\r" + '<' + str(sock.getpeername()) + '> ' + data)
                except:

                    broadcast_data(sock,'Client(%s,%s) is offline'% addr)
                    print("Client (%s, %s) is offline" % addr)
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
        read_sockets.close()




