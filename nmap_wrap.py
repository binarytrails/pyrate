import os

class NmapWrap:
    def __init__(self, target_ip):
        self.nmap_command = "nmap -sC -sV -oG /tmp/nmapscan {ip}"
        self.target_ip = target_ip

    def run(self):
        command = self.nmap_command.format(ip=self.target_ip)
        os.system(command)