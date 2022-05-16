import os
import argparse


class ArgParser:
    def __init__(self, args):
        self.args_parser = argparse.ArgumentParser()

        self.args_parser.add_argument('-j', dest='jpg', help='jpg file',
                                      required=False)
        self.args_parser.add_argument('-m', dest='mp4', help='mp4 file',
                                      required=False)
        self.args_parser.add_argument('-g', dest='gif', help='gif file',
                                      required=False)
        self.args_parser.add_argument('-o', dest='out',
                                      help='Path to output file',
                                      required=True)
        self.args_parser.add_argument('-s', dest='scale',
                                      help='Ratio between input and output '
                                           'files, can\'t be more than 1 or '
                                           'less than 0',
                                      required=False)

        self._args = self.parse_args(args)

        self.jpg = self._args.jpg
        self.mp4 = self._args.mp4
        self.gif = self._args.gif

        self.scale = self._args.scale
        self.out = self._args.out

    def parse_args(self, args):
        return self.args_parser.parse_args(args)

    def get_destination_path(self, filename):
        return os.path.join('out',
                            os.path.basename(self.image).split('.')[
                                0] + '_result.txt')
