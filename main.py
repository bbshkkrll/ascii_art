import sys

from arg_parser import ArgParser
from saver import Saver

if __name__ == '__main__':
    parser = ArgParser(sys.argv[1:])

    saver = Saver(parser.file, parser.out, parser.name)
    saver.save()
