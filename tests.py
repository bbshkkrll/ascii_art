import os.path
import sys
import unittest

from PIL import Image

from converter import Converter
from saver import Saver


class SaverTest(unittest.TestCase):

    def test_exists_file_png(self):
        saver = Saver(os.path.join('in', 'skull.png'), 'out', 'skull')
        saver.save()

        self.assertTrue(
            os.path.exists(os.path.join(os.path.join('out', 'skull.png'))))

    def test_exists_file_jpg(self):
        saver = Saver(os.path.join('in', 'jamal.jpg'), 'out', 'jamal')
        saver.save()

        self.assertTrue(
            os.path.exists(os.path.join(os.path.join('out', 'jamal.jpg'))))

    def test_exists_file_gif(self):
        saver = Saver(os.path.join('in', 'anime-dance-happy.gif'), 'out',
                      'anime')
        saver.save()

        self.assertTrue(
            os.path.exists(os.path.join(os.path.join('out', 'anime.gif'))))

    def test_exists_file_mp4(self):
        saver = Saver(os.path.join('in', 'mp4.mp4'), 'out', 'mp4')
        saver.save()

        self.assertTrue(
            os.path.exists(os.path.join(os.path.join('out', 'mp4.mp4'))))

    def test_value_error_with_incorrect_format(self):
        saver = Saver('.', '', '')

        self.assertRaises(ValueError, saver.save)


class ConverterTest(unittest.TestCase):
    def test_convert_to_ascii(self):
        converter = Converter()
        converter.set_scale(1)

        img, mode = converter.convert_to_ascii(
            Image.new('RGB', (1, 1), (0, 0, 0)), 1)

        self.assertListEqual(['$'], img)
        self.assertEqual('RGB', mode)

    def test_create_frame(self):
        converter = Converter()
        converter.set_scale(1)
        img = converter.create_frame(['$$',
                                      '$$'], 'RGB')

        self.assertEqual(img.mode, 'RGB')
        self.assertTupleEqual(img.size, (16, 16))

        img_rgba = converter.create_frame(['$$$',
                                           '$$$',
                                           '$$$'], 'RGBA')

        self.assertEqual(img_rgba.mode, 'RGBA')
        self.assertTupleEqual(img_rgba.size, (24, 24))

    def test_set_scale_sys_exit(self):
        converter = Converter()
        converter.set_scale(1000)

        with self.assertRaises(SystemExit):
            converter.convert_to_ascii([], 1)


if __name__ == '__main__':
    unittest.main()
