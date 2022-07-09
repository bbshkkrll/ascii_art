import argparse


class ArgParser:
    def __init__(self, args):
        self.args_parser = argparse.ArgumentParser()

        self.args_parser.add_argument('-f', dest='file',
                                      help='Filename of input file',
                                      required=True)
        self.args_parser.add_argument('-o', dest='out',
                                      help='Path to output file',
                                      required=True)
        self.args_parser.add_argument('-s', dest='scale',
                                      help='Ratio between input and output '
                                           'files, can\'t be more than 1 or '
                                           'less than 0',
                                      required=False)
        self.args_parser.add_argument('-n', dest='name',
                                      help='Name of output file',
                                      required=True)

        self._args = self.args_parser.parse_args(args)

        self.name = self._args.name.split('.')[0]
        self.file = self._args.file
        self.scale = self._args.scale
        self.out = self._args.out
