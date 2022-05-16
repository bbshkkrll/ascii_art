import multiprocessing
import os.path
import sys

import cv2
import numpy as np
from PIL import Image
from converter import Converter


# converter = Converter()
# converter.set_scale(0.5)

#
# def convert(img):
#     txt, mode = converter.convert_to_ascii(img, 1)
#     converter.create_frame(txt, mode)
#
#
# def save_gif(response):
#     response[0].save("ttt.gif", format='GIF',
#                      append_images=response,
#                      save_all=True, duration=200, loop=0)

#
# def end_func(response):
#     codec = cv2.VideoWriter_fourcc(*'MPEG')
#
#     writer = cv2.VideoWriter('out\\mama.mp4', codec, 24,
#                              response[0].size)
#     for img in response:
#         writer.write(np.array(img))
#
#     writer.release()


def print_name():
    print(__name__)


class VideoSaver:
    def __init__(self, filename, out_path):
        cap = cv2.VideoCapture(filename)

        self.converter = Converter()
        self.converter.set_scale(0.35)
        self.out_path = out_path
        self.frames_count = int(cap.get(7))
        self.fps = int(cap.get(5))
        self.frames = [] * self.frames_count
        self.format = filename.split('.')[-1]
        self.duration = self.frames_count // self.fps

        while cap.isOpened():
            _, frame = cap.read()

            if frame is None:
                break

            self.frames.append(Image.fromarray(frame))

        cap.release()

    def save_as_gif(self, frames):
        if frames is None or frames[0] is None or self.format != 'gif':
            return

        frames[0].save(self.out_path,
                       format='GIF',
                       append_images=frames,
                       save_all=True, duration=self.duration, loop=0)

    def save_as_mp4(self, frames):
        fourcc = cv2.VideoWriter_fourcc(*'MPEG')

        writer = cv2.VideoWriter(
            self.out_path, fourcc,
            self.fps,
            frames[0].size)
        for frame in frames:
            writer.write(np.array(frame))

        writer.release()

    def wrap_converter(self, frame):
        return self.converter.create_frame(
            *self.converter.convert_to_ascii(frame, 1))

    def save(self):

        if self.format == 'mp4':
            with multiprocessing.Pool(multiprocessing.cpu_count() * 3) as p:
                p.map_async(self.wrap_converter, self.frames,
                            callback=self.save_as_mp4)
                p.close()
                p.join()
        elif self.format == 'gif':
            with multiprocessing.Pool(multiprocessing.cpu_count() * 3) as p:
                p.map_async(self.wrap_converter, self.frames,
                            callback=self.save_as_gif)
                p.close()
                p.join()
        else:
            raise ValueError(f'Не поддерживаемый формат{self.format}')

# if __name__ == '__main__':

# cap = cv2.VideoCapture('in\\2ull.gif')
# frames = [] * int(cap.get(7))
# print(cap.get(5))
# while cap.isOpened():
#     _, frame = cap.read()
#
#     if frame is None:
#         break
#
#     frames.append(Image.fromarray(frame))
#
# with multiprocessing.Pool(multiprocessing.cpu_count() * 3) as p:
#     p.map_async(convert, frames, callback=save_gif)
#     p.close()
#     p.join()

if __name__ == '__main__':
    saver = VideoSaver('in\\cat.gif', 'out\\1.gif')
    saver.save()
