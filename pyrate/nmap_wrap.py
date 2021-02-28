# @author dotPY-hax
# @author Vsevolod Ivanov

import os

class NmapWrap:
    def __init__(self, rhost):
        self.nmap_command = 'nmap -sC -sV -oG /tmp/nmapscan {ip}'
        self.rhost = rhost

    def run(self):
        command = self.nmap_command.format(ip=self.rhost)
        os.system(command)
