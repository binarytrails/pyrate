# @author dotPY-hax
# @author Vsevolod Ivanov

import argparse
import traceback

from pyrate.cli import CLI
from pyrate.reverse_shell import ReverseShell
from pyrate.nmap_wrap import NmapWrap

__version__ = '0.1'
__authors__ = 'dotPY-hax, vsevolod ivanov'
__description__ = 'pyrate - simple pentest tools'
__banner__ = u"""
█ ▄▄ ▀▄    ▄ █▄▄▄▄ ██     ▄▄▄▄▀ ▄███▄
█   █  █  █  █  ▄▀ █ █ ▀▀▀ █    █▀   ▀
█▀▀▀    ▀█   █▀▀▌  █▄▄█    █    ██▄▄
█       █    █  █  █  █   █     █▄   ▄▀
 █    ▄▀       █      █  ▀      ▀███▀
  ▀           ▀      █
                    ▀
"""

def get_parser():
    parser = argparse.ArgumentParser('\n'.join(['', __banner__ + __description__, 'by ' + __authors__, '']))
    parser.add_argument('--version', '-v', action='version', version=__version__)
    parser.add_argument('--rhost', '-r', type=str, default=None)
    parser.add_argument('--lhost', '-l', type=str, default='0.0.0.0')
    parser.add_argument('--lport', '-p', type=int, default=42069)
    return parser

class Pyrate:

    def __init__(self, lhost, lport, rhost):
        self.cli = CLI()
        self.cli.prompt_text = '$'
        self.running = True

        self.lhost = lhost
        self.lport = lport
        self.rhost = rhost

    def main_loop(self):
        print(__banner__ + 'select an action (h=help)')
        while self.running:
            try:
                prompt = self.cli.cli_prompt()
                self.handle_command(prompt)
            except KeyboardInterrupt as e:
                key = input(' do you want to quit (y)? ')
                if (key == 'y'):
                    break

    def handle_command(self, prompt):
        p = prompt.lower()
        if p == 'r':
            self.start_reverse_shell()
        elif p == 'n':
            self.start_nmap_wrap()
        elif p == 'q':
            self.running = False
        elif p == 'h' or p == '?':
            print('actions: [r]everse, [n]map, [h]elp, [q]uit')

    def start_reverse_shell(self):
        stop = False
        while not stop:
            rshell = None
            try:
                rshell = ReverseShell(self.lhost, self.lport, self.rhost)
                rshell.main_loop()
            except KeyboardInterrupt as e:
                key = input(' do you want to stop (y)? ')
                if (key == 'y'):
                    stop = True
            except BrokenPipeError as e:
                print(e)
            except ConnectionResetError as e:
                print(e)
            except OSError as e:
                print(e)
            if (rshell):
                del rshell
            if (not stop):
                print('restarting reverse shell..')

    def start_nmap_wrap(self):
        nmap_wrap = NmapWrap(self.rhost)
        nmap_wrap.run()
