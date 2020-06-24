import socket
import select


class PortListener:
    def __init__(self, host_ip, port_number):
        self.port = port_number
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host_ip, port_number))
        self._listen()
        self._accept()
        self.socket.setblocking(False)

    def close(self):
        self.socket.close()

    def _listen(self):
        self.socket.listen(5)
        print("Listening on {}".format(self.port))

    def _accept(self):
        self.connection, address = self.socket.accept()
        self.target_ip = address[0]
        print("Connection to {} established".format(self.target_ip))

    def receive_data(self):
        byte_data = b""
        while select.select([self.connection], [], [], 0.5)[0]:
            received = self.connection.recv(1)
            byte_data += received
        string_data = str(byte_data, encoding="utf-8")
        list_of_string_data = string_data.split("\n")
        return list_of_string_data

    def send_data(self, data_to_send):
        byte_data = bytes(data_to_send, encoding="utf-8")
        string_data = str(byte_data)
        self.connection.sendall(byte_data)

    def send_receive(self, data_to_send):
        self.send_data(data_to_send)
        data_received = self.receive_data()
        return data_received

    def wait_for_data(self):
        self.receive_data()
