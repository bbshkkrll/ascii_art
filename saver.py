import os.path


# img = Image.open('in\\skull.png')
#
# converter = AsciiImage()
# converter.set_scale(0.2)
# ascii_img = converter.convert_to_ascii(img, 1)
#
# _PIXEL_SCALE = 6
#
# rows, cols = len(ascii_img), len(ascii_img[0])
#
# if img.format != 'PNG':
#     output_image = Image.new("RGB", (
#         cols * _PIXEL_SCALE, rows * _PIXEL_SCALE))
#     mode = 'RGB'
# else:
#     output_image = Image.new("RGBA", (
#         cols * _PIXEL_SCALE, rows * _PIXEL_SCALE))
#     mode = 'RGBA'
#
# draw_image = ImageDraw.Draw(output_image)
#
# for row in range(rows):
#     for col in range(cols):
#         if ascii_img[row][col] == '=':
#             draw_image.text(
#                 (col * _PIXEL_SCALE, row * _PIXEL_SCALE),
#                 ' ')
#         else:
#             draw_image.text(
#                 (col * _PIXEL_SCALE, row * _PIXEL_SCALE),
#                 ascii_img[row][col])
#
# # output = Image.fromarray(np.array(output_image), mode)
# output_image.save(f'out\\kikikiki___.{img.format.lower()}', img.format)


class Saver:
    @staticmethod
    def save_image(img, name):
        frmt = 'JPEG'
        if img.mode == 'RGBA':
            frmt = 'PNG'
        img.save(
            os.path.join(os.getcwd(), 'out',
                         f'{name}.{frmt.lower()}'), frmt)
