import sys
import numpy as np
from PIL import Image, ImageDraw

from saver import Saver


class Converter:
    _SCALE = 0.3
    _GRAY_SCALE = \
        "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvu" + \
        "nxrjft/|\\()1{}[]?-_+~<>i!lI;:,\"^`'. "

    _INVISIBLE_PIXEL = '='
    _PIXEL_SCALE = 8

    def set_scale(self, scale):
        self._SCALE = float(scale)

    def get_average_gray(self, image_part):
        image_arr = np.array(image_part.convert('L'))
        return int(np.average(image_arr))

    def get_average_alpha(self, image):
        image_rgba = np.array(image.convert('RGBA').split()[-1])
        if np.average(image_rgba) < 255:
            return self._INVISIBLE_PIXEL
        return self.get_average_gray(image)

    def convert_to_ascii(self, image, rows_factor):

        if self._SCALE > 1 or self._SCALE < 0:
            sys.exit()

        if image.format == 'PNG':
            image = image.convert('RGBA')

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

                if image.mode == 'RGBA':
                    avg = self.get_average_alpha(
                        image.crop((x_start, y_start, x_end, y_end)))
                else:
                    avg = self.get_average_gray(
                        image.crop((x_start, y_start, x_end, y_end)))

                if avg != '=':
                    ascii_image[row] += self._GRAY_SCALE[
                        int((avg * len(self._GRAY_SCALE) - 1) / 255)]
                else:
                    ascii_image[row] += avg
        return ascii_image, image.mode

    def create_frame(self, txt_list, mode):

        rows, cols = len(txt_list), len(txt_list[0])

        # if mode == 'PNG':
        #     created_image = Image.new("RGBA", (
        #         cols * self._PIXEL_SCALE, rows * self._PIXEL_SCALE))
        # else:
        #     created_image = Image.new("RGB", (
        #         cols * self._PIXEL_SCALE, rows * self._PIXEL_SCALE))

        created_image = Image.new(mode, (
                    cols * self._PIXEL_SCALE, rows * self._PIXEL_SCALE))

        draw_image = ImageDraw.Draw(created_image)

        for row in range(rows):
            for col in range(cols):
                if txt_list[row][col] == '=':
                    draw_image.text(
                        (col * self._PIXEL_SCALE, row * self._PIXEL_SCALE),
                        ' ')
                else:
                    draw_image.text(
                        (col * self._PIXEL_SCALE, row * self._PIXEL_SCALE),
                        txt_list[row][col])

        return created_image


if __name__ == '__main__':
    converter = Converter()
    converter.set_scale(0.1)
    txt, frmt = converter.convert_to_ascii(Image.open('in\\navalych.jpg'), 1)
    saver = Saver()
    saver.save_image(converter.create_frame(txt, frmt), 'gnida')
