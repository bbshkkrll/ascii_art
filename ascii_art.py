import sys
import numpy as np


class AsciiImage:
    _SCALE = 0.3
    _GRAY_SCALE = \
        "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvu" + \
        "nxrjft/|\\()1{}[]?-_+~<>i!lI;:,\"^`'. "

    def set_scale(self, scale):
        self._SCALE = float(scale)

    @staticmethod
    def get_average_gray(image_part):
        image_arr = np.array(image_part.convert('L'))
        return int(np.average(image_arr))

    def convert_to_ascii(self, image, rows_factor):
        if self._SCALE > 1 or self._SCALE < 0:
            sys.exit()

        width, height = image.size[0], image.size[1]
        cols = int(width * self._SCALE)
        rows = int(height * self._SCALE * rows_factor)
        width_part = width / cols
        height_part = height / rows

        ascii_image = []

        for row in range(rows):
            y_start = int(row * height_part)
            y_end = int((row + 1) * height_part)

            if row == rows - 1:
                y_end = height
            ascii_image.append('')

            for col in range(cols):
                x_start = int(col * width_part)
                x_end = int((col + 1) * width_part)

                if col == cols - 1:
                    x_end = width

                avg = self.get_average_gray(
                    image.crop((x_start, y_start, x_end, y_end)))

                ascii_image[row] += self._GRAY_SCALE[
                    int((avg * len(self._GRAY_SCALE) - 1) / 255)]

        return ascii_image
