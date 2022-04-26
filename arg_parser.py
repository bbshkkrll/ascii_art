import os
import argparse


class ArgParser:
    def __init__(self, args):
        self.args_parser = argparse.ArgumentParser()

        self.args_parser.add_argument('-i', dest='image',
                                      help='path to .jpg file', required=False)
        self.args_parser.add_argument('-v', dest='video', required=False)
        self.args_parser.add_argument('-o', dest='out',
                                      help='path to out.txt file, '
                                           'default: out{filename}_ascii.txt)',
                                      required=False)
        self.args_parser.add_argument('-s', dest='scale',
                                      help='scale of resulting ascii image',
                                      required=False)

        self._args = self.parse_args(args)

        self.image = self._args.image
        self.video = self._args.video
        self.scale = self._args.scale
        if self.image:
            self.out = self.get_destination_path(self._args.out)

    def parse_args(self, args):
        return self.args_parser.parse_args(args)

    def get_destination_path(self, filename):
        if filename:
            return filename

        return os.path.join('out',
                            os.path.basename(self.image).split('.')[
                                0] + '_result.txt')
