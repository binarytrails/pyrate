class PrivilegeEscalation:
    def __init__(self, reverse_shell):
        self.reverse_shell = reverse_shell

    def _run_and_get_result(self, command):
        command += "\n"
        result = self.reverse_shell.run_command_and_print(command)
        return result

    def look_for_sudo(self):
        command = "sudo -l"
        result = self._run_and_get_result(command)

    def look_for_suid(self):
        command = "find / -perm -u=s -type f 2>/dev/null"
        result = self._run_and_get_result(command)

    def search_for_privesc(self):
        self.look_for_sudo()
        self.look_for_suid()
