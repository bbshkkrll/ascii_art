import multiprocessing
import os
import cv2
import numpy as np

from PIL import Image
from converter import Converter


class Saver:
    def __init__(self, path, out_path, result_name):

        self.path = path
        self.converter = Converter()
        self.converter.set_scale(0.2)
        self.out_name = result_name
        self.out_path = out_path

        self.duration = None
        self.frames = None
        self.fps = None
        self.frames_count = None

        self.filename, self.ext = os.path.splitext(path)
        if self.ext == '.mp4' or self.ext == '.gif':
            self.get_frames(self.path)

    def get_frames(self, path):
        cap = cv2.VideoCapture(path)

        self.frames_count = int(cap.get(7))
        self.fps = int(cap.get(5))
        self.frames = [] * self.frames_count
        self.duration = self.frames_count // self.fps

        while cap.isOpened():
            _, frame = cap.read()

            if frame is None:
                break

            self.frames.append(Image.fromarray(frame))

        cap.release()

    def save_as_gif(self, frames):
        if frames is None or frames[0] is None or self.ext != '.gif':
            raise ValueError

        frames[0].save(
            os.path.join(self.out_path, f'{self.out_name}{self.ext}'),
            format='GIF',
            append_images=frames,
            save_all=True, duration=self.duration, loop=0)

    def save_as_mp4(self, frames):
        fourcc = cv2.VideoWriter_fourcc(*'MPEG')

        writer = cv2.VideoWriter(
            os.path.join(self.out_path, f'{self.out_name}{self.ext}'), fourcc,
            self.fps,
            frames[0].size)
        for frame in frames:
            writer.write(np.array(frame))

        writer.release()

    def save_image(self, img):
        # img = img.resize((img.size[0] // 4, img.size[1] // 4))
        img.save(os.path.join(self.out_path,
                              f'{self.out_name}{self.ext}'),
                 img.format)

    def wrap_converter(self, frame):
        return self.converter.create_frame(
            *self.converter.convert_to_ascii(frame, 1))

    def save(self):

        if self.ext == '.mp4':
            with multiprocessing.Pool(multiprocessing.cpu_count() * 3) as p:
                p.map_async(self.wrap_converter, self.frames,
                            callback=self.save_as_mp4)
                p.close()
                p.join()
        elif self.ext == '.gif':
            with multiprocessing.Pool(multiprocessing.cpu_count() * 3) as p:
                p.map_async(self.wrap_converter, self.frames,
                            callback=self.save_as_gif)
                p.close()
                p.join()

        elif self.ext == '.jpg' or self.ext == '.jpeg' or self.ext == '.png':
            ascii_img = self.wrap_converter(Image.open(self.path))
            self.save_image(ascii_img)

        else:
            raise ValueError(f'Не поддерживаемый формат: {self.ext}')
