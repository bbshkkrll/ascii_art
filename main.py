import os.path

from video_saver import VideoSaver

if __name__ == '__main__':
    saver = VideoSaver('in\\anime-dance-happy.gif', 'out\\2.gif')
    saver.save()
