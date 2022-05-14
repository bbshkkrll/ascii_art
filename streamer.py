# import sys
# import cv2
# import numpy as np
#
# from PIL import ImageDraw, Image
# from converter import AsciiImage
#
#
# class AsciiVideo:
#     _PIXEL_SCALE = 8
#
#     def __init__(self, filename, scale):
#         self.cap = cv2.VideoCapture(filename)
#         self.Converter = AsciiImage()
#         if scale is not None:
#             self.Converter.set_scale(scale)
#         else:
#             self.Converter.set_scale(0.15)
#
#     def convert_to_ascii(self):
#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#         out = cv2.VideoWriter('out\\111.mp4', fourcc, 1, (180, 320))
#         while self.cap.isOpened():
#             _, frame = self.cap.read()
#             # out.write(frame)
#             if frame is None:
#                 sys.exit()
#
#             img = self.Converter.convert_to_ascii(Image.fromarray(frame), 1)
#
#             rows, cols = len(img), len(img[0])
#             # print(f'{cols * self._PIXEL_SCALE}, {rows * self._PIXEL_SCALE}')
#             output_image = Image.new("RGB", (
#                 cols * self._PIXEL_SCALE, rows * self._PIXEL_SCALE))
#             ascii_img = ImageDraw.Draw(output_image)
#
#             for row in range(rows):
#                 for col in range(cols):
#                     if img[row][col] == '=':
#                         ascii_img.text(
#                             (col * self._PIXEL_SCALE, row * self._PIXEL_SCALE),
#                             ' ')
#                     else:
#                         ascii_img.text(
#                             (col * self._PIXEL_SCALE, row * self._PIXEL_SCALE),
#                             img[row][col])
#
#             img = Image.fromarray(np.array(output_image))
#             img.save('out\\result1.png', 'PNG')
#             output_image = np.array(output_image)
#
#             if cv2.waitKey(1) == ord("q"):
#                 break
#             cv2.imshow("Result", output_image)
#
#         # self.cap.release()
#         # cv2.destroyAllWindows()
