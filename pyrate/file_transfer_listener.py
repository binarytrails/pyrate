# @author dotPY-hax
# @author Vsevolod Ivanov

import select
import socket

class PortFileTransfer:
    def __init__(self, host_ip, port_number, target_ip):
        self.port = port_number
        self.socket = socket.socket()
        self.target_ip = target_ip
        self.connection = None
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host_ip, port_number))

    def receive_data(self):
        byte_data = b''
        while select.select([self.connection], [], [], 1)[0]:
            received = self.connection.recv(1)
            byte_data += received
        return byte_data

    def send_data(self, data_to_send):
        self.connection.sendall(data_to_send)

    def connect(self):
        self.socket.connect((self.target_ip, self.port))
        self.socket.setblocking(False)

    def get_connected(self):
        self.socket.listen(5)
        self.connection, address = self.socket.accept()
        self.target_ip = address[0]
        self.socket.setblocking(False)
        print('Connection to {} established'.format(self.target_ip))

    def close(self):
        self.socket.close()
