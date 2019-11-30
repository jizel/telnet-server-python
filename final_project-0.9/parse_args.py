from ConfigParser import SafeConfigParser
from ConfigParser import NoSectionError
import argparse

def get_args_from_line(h, port, maxuser, reg_file, *reg_exp):
    d = {}
    if h:
        d['host'] = h
    if port:
        d['port'] = port
    if maxuser:
        d['maxuser'] = maxuser
    if reg_file:
        d['reg_file'] = reg_file
    if reg_exp != (None,):
        d['reg_exp'] = []
        for reg in reg_exp:
            d['reg_exp'].extend(reg)

    return d


def get_args_from_file(*conf_files):
    d = {}
    parser = SafeConfigParser()
    for conf_file in conf_files:
        parser.read(conf_file)
        try:
            options = parser.options('server')
        except NoSectionError:
            return d
        for option in options:
            if option not in d:
                if option == 'maxuser':
                    # Int value - needs special treatment
                    d[option] = int(parser.get('server', option))
                if option == 'reg_exp':
                    # Array of strings
                    d[option] = str(parser.get('server', option)).split()

                else:
                    d[option] = parser.get('server', option)
    return d


def merge_args(d1, d2):
    out_d = d1
    for key in d2:
        if key not in d1:
            out_d[key] = d2.get(key)
        elif key in d1 and key == 'reg_exp':
            out_d[key] = d1.get(key) + d2.get(key)
    return out_d

argparser = argparse.ArgumentParser(description="Parser for final.py. Any unknown args are considered as config files.")
argparser.add_argument(
    "-H",
    "--host",
)
argparser.add_argument(
    "-p",
    "--port",
)
argparser.add_argument(
    "-R",
    "--reg",
    nargs='*',
    help='Regular expressions to be added'
)
argparser.add_argument(
    "conf_files",
    nargs='*',
    type=str,
    help='List of configuration files. Each file has to have a [server] section!'
)
argparser.add_argument(
    "--maxuser",
    "-MU",
    type=int,
    help='Number of maximum concurrent connections'
)
argparser.add_argument(
    "--reg_file",
    "-RF",
    help='External file for regular expressions'
)

args = argparser.parse_args()

args_from_line = get_args_from_line(args.host, args.port,args.maxuser, args.reg_file, args.reg)
print "Args from command line: %s" % args_from_line

args_from_file = get_args_from_file(args.conf_files)
print "Args from config files: %s" % args_from_file

all_args = merge_args(args_from_line, args_from_file)
print "Final arguments used: %s" % all_args

if 'reg_exp' in all_args:
    print "Used reg expressions: %s" % all_args['reg_exp']


def get_complete_args():
    return all_args


