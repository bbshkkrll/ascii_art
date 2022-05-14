import multiprocessing
import cv2
import numpy as np
from PIL import Image, ImageDraw
from converter import AsciiImage

converter = AsciiImage()


def convert(img):
    return converter.convert_to_ascii(img, 1)


def save_gif(response):
    _PIXEL_SCALE = 8

    rows, cols = len(response[0]), len(response[0][0])

    frames = []
    for img in response:

        output_image = Image.new("RGB", (
            cols * _PIXEL_SCALE, rows * _PIXEL_SCALE))

        ascii_img = ImageDraw.Draw(output_image)

        for row in range(rows):
            for col in range(cols):
                if img[row][col] == '=':
                    ascii_img.text(
                        (col * _PIXEL_SCALE, row * _PIXEL_SCALE),
                        ' ')
                else:
                    ascii_img.text(
                        (col * _PIXEL_SCALE, row * _PIXEL_SCALE),
                        img[row][col])

        frames.append(output_image)

    frame = frames[0]
    frame.save("ya_ne_mogu_naxui.gif", format='GIF', append_images=frames,
               save_all=True, duration=80, loop=0)


def end_func(response):
    _PIXEL_SCALE = 8

    codec = cv2.VideoWriter_fourcc(*'MPEG')

    rows, cols = len(response[0]), len(response[0][0])

    writer = cv2.VideoWriter('out\\5.mp4', codec, 12,
                             (cols * _PIXEL_SCALE, rows * _PIXEL_SCALE))

    frames = []
    for img in response:

        output_image = Image.new("RGB", (
            cols * _PIXEL_SCALE, rows * _PIXEL_SCALE))

        ascii_img = ImageDraw.Draw(output_image)

        for row in range(rows):
            for col in range(cols):
                if img[row][col] == '=':
                    ascii_img.text(
                        (col * _PIXEL_SCALE, row * _PIXEL_SCALE),
                        ' ')
                else:
                    ascii_img.text(
                        (col * _PIXEL_SCALE, row * _PIXEL_SCALE),
                        img[row][col])

        writer.write(np.array(output_image))

    cap.release()
    writer.release()


if __name__ == '__main__':

    cap = cv2.VideoCapture('in\\mp4.mp4')
    frames = [] * int(cap.get(7))
    print(cap.get(5))
    while cap.isOpened():
        _, frame = cap.read()

        if frame is None:
            break

        frames.append(Image.fromarray(frame))

    with multiprocessing.Pool(multiprocessing.cpu_count() * 3) as p:
        p.map_async(convert, frames, callback=end_func)
        p.close()
        p.join()

