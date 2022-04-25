import argparse
import os
import sys
import numpy as np
import webbrowser
import cv2

from PIL import Image


class AsciiImageCV2:
    _SCALE = 0.4
    _GRAY_SCALE = \
        "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvu" + \
        "nxrjft/|\\()1{}[]?-_+~<>i!lI;:,\"^`'. "

    def __init__(self, image):
        self.image = cv2.flip(cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE), 1)
        self.w, self.h, _ = self.image.shape
        self.cols = int(self.w * self._SCALE)
        # self.rows = int(self.h * self._SCALE / 2)
        self.rows = int(self.h * self._SCALE)

    def set_scale(self, scale):
        self._SCALE = float(scale)

    def rotate(self, image, angle):
        (h, w) = image.shape[:2]
        center = (int(w / 2), int(h / 2))
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
        return cv2.warpAffine(image, rotation_matrix, (w, h))

    def get_average_gray(self, pixel):
        image_arr = np.array(pixel)
        w, h, _ = image_arr.shape
        return int(np.average(image_arr.reshape(w * h * _)))

    def crop_image(self, x_start, y_start, x_end, y_end):
        return self.image[x_start:x_end, y_start:y_end]

    def convert_to_ascii(self):
        if self._SCALE > 1 or self._SCALE < 0:
            sys.exit(0)

        cols = int(self.w * self._SCALE)
        rows = int(self.h * self._SCALE)
        w_part = self.w / cols
        h_part = self.h / rows

        ascii_image = []

        for row in range(rows):
            y_start = int(row * h_part)
            y_end = int((row + 1) * h_part)

            if row == rows - 1:
                y_end = self.h
            ascii_image.append('')

            for col in range(cols):
                x_start = int(col * w_part)
                x_end = int((col + 1) * w_part)

                if col == cols - 1:
                    x_end = self.w

                avg = self.get_average_gray(
                    self.crop_image(x_start, y_start, x_end, y_end))

                ascii_image[row] += self._GRAY_SCALE[
                    int((avg * len(self._GRAY_SCALE) - 1) / 255)]

        return ascii_image


class AsciiImage:
    _SCALE = 0.3
    _GRAY_SCALE = \
        "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvu" + \
        "nxrjft/|\\()1{}[]?-_+~<>i!lI;:,\"^`'. "

    def __init__(self, image):
        self.image = image

    def set_scale(self, scale):
        self._SCALE = float(scale)

    def get_average_gray(self, image_part):
        image_arr = np.array(image_part)
        w, h = image_arr.shape
        return int(np.average(image_arr.reshape(w * h)))

    def convert_to_ascii(self):
        if self._SCALE > 1 or self._SCALE < 0:
            sys.exit(0)

        w, h = self.image.size[0], self.image.size[1]
        cols = int(w * self._SCALE)
        rows = int(h * self._SCALE / 2)
        w_part = w / cols
        h_part = h / rows

        ascii_image = []

        for row in range(rows):
            y_start = int(row * h_part)
            y_end = int((row + 1) * h_part)

            if row == rows - 1:
                y_end = h
            ascii_image.append('')

            for col in range(cols):
                x_start = int(col * w_part)
                x_end = int((col + 1) * w_part)

                if col == cols - 1:
                    x_end = w

                avg = self.get_average_gray(
                    self.image.crop((x_start, y_start, x_end, y_end)))

                ascii_image[row] += self._GRAY_SCALE[
                    int((avg * len(self._GRAY_SCALE) - 1) / 255)]

        return ascii_image


class ArgParser:
    def __init__(self, args):
        self.args_parser = argparse.ArgumentParser()

        self.args_parser.add_argument('-i', dest='image',
                                      help='path to .jpg file', required=True)
        self.args_parser.add_argument('-o', dest='out',
                                      help='path to out.txt file, '
                                           'default: out{image_name}_ascii.txt)',
                                      required=False)
        self.args_parser.add_argument('-s', dest='scale',
                                      help='scale of resulting ascii image',
                                      required=False)

        self._args = self.parse_args(args)

        self.image = self._args.image
        self.scale = self._args.scale
        self.out = self.get_destination_path(self._args.out)

    def parse_args(self, args):
        return self.args_parser.parse_args(args)

    def get_destination_path(self, filename):
        if filename:
            return filename

        return os.path.join('out',
                            os.path.basename(self.image).split('.')[
                                0] + '_result.txt')


def main():
    parser = ArgParser(sys.argv[1:])
    # image = AsciiImage(Image.open(parser.image).convert('L'))
    image = AsciiImageCV2(
        cv2.cvtColor(cv2.imread(parser.image), cv2.COLOR_BGR2GRAY))

    if parser.scale:
        image.set_scale(parser.scale)

    ascii_img = image.convert_to_ascii()

    with open(parser.out, 'w', encoding='utf-8') as f:
        for line in ascii_img:
            f.write(line + '\n')

    print(parser.out)
    webbrowser.open(parser.out)


if __name__ == '__main__':
    main()
