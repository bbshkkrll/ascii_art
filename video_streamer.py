import sys
import cv2
import numpy as np

from PIL import ImageDraw, Image
from ascii_art import AsciiImage


class AsciiVideo:
    def __init__(self, filename, scale):
        self.cap = cv2.VideoCapture(filename)
        self.Converter = AsciiImage()
        if scale is not None:
            self.Converter.set_scale(scale)
        else:
            self.Converter.set_scale(0.15)

    def convert_to_ascii(self):
        while self.cap.isOpened():
            _, frame = self.cap.read()

            if frame is None:
                sys.exit()

            img = self.Converter.convert_to_ascii(Image.fromarray(frame), 1)

            rows, cols = len(img), len(img[0])

            output_image = Image.new("RGB", (cols * 5, rows * 5))
            ascii_img = ImageDraw.Draw(output_image)

            for row in range(rows):
                for col in range(cols):
                    ascii_img.text((col * 5, row * 5), img[row][col])

            output_image = np.array(output_image)

            if cv2.waitKey(1) == ord("q"):
                break

            cv2.imshow("Result", output_image)

        self.cap.release()
        cv2.destroyAllWindows()
