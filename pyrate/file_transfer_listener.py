# @author dotPY-hax
# @author Vsevolod Ivanov

import select
import socket

class PortFileTransfer:
    def __init__(self, lhost, lport, rhost):
        self.port = lport
        self.socket = socket.socket()
        self.rhost = rhost
        self.connection = None
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print('[portfiletransfer] bind {}:{}'.format(lhost, lport))
        self.socket.bind((lhost, lport))
        print('[portfiletransfer] binded')

    def receive_data(self):
        byte_data = b''
        while select.select([self.connection], [], [], 1)[0]:
            received = self.connection.recv(1)
            if (received.decode()):
                print(received)
            byte_data += received
        return byte_data

    def send_data(self, data_to_send):
        self.connection.sendall(data_to_send)

    def connect(self):
        self.socket.connect((self.rhost, self.port))
        self.socket.setblocking(False)

    def get_connected(self):
        self.socket.listen(5)
        print('[portfiletransfer] listening')
        self.connection, address = self.socket.accept()
        print('[portfiletransfer] accepted')
        self.rhost = address[0]
        self.socket.setblocking(False)
        print('Connection to {} established'.format(self.rhost))

    def close(self):
        self.socket.close()
