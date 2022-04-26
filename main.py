import sys
import webbrowser

from PIL import Image
from arg_parser import ArgParser
from ascii_art import AsciiImage
from video_streamer import AsciiVideo


def main():
    parser = ArgParser(sys.argv[1:])

    if parser.image:
        image = AsciiImage()

        if parser.scale:
            image.set_scale(parser.scale)

        ascii_img = image.convert_to_ascii(Image.open(parser.image), 0.5)

        with open(parser.out, 'w', encoding='utf-8') as f:
            for line in ascii_img:
                f.write(line + '\n')

        print(parser.out)
        webbrowser.open(parser.out)

    if parser.video:
        AsciiVideo(parser.video, parser.scale).convert_to_ascii()


if __name__ == '__main__':
    main()
