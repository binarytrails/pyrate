# @author Vsevolod Ivanov <seva@binarytrails.net>

from pyrate import pyrate

if __name__ == '__main__':
    args = pyrate.get_parser().parse_args()
    pyr = pyrate.Pyrate(args.lhost, args.lport, args.rhost)
    pyr.main_loop()
