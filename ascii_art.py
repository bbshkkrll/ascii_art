import argparse
import os
import sys
import numpy as np
import webbrowser
import cv2

from PIL import Image


class AsciiImage:
    _SCALE = 0.3
    _GRAY_SCALE = \
        "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvu" + \
        "nxrjft/|\\()1{}[]?-_+~<>i!lI;:,\"^`'. "

    def set_scale(self, scale):
        self._SCALE = float(scale)

    def get_average_gray(self, image_part):
        image_arr = np.array(image_part.convert('L'))
        return int(np.average(image_arr))

    def convert_to_ascii(self, image, rows_factor):
        if self._SCALE > 1 or self._SCALE < 0:
            sys.exit(0)

        w, h = image.size[0], image.size[1]
        cols = int(w * self._SCALE)
        rows = int(h * self._SCALE * rows_factor)
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
                    image.crop((x_start, y_start, x_end, y_end)))

                ascii_image[row] += self._GRAY_SCALE[
                    int((avg * len(self._GRAY_SCALE) - 1) / 255)]

        return ascii_image
