import os

from yt_concate.settings import CAPTIONS_DIR
from yt_concate.settings import VIDEOS_DIR
from yt_concate.settings import DOWNLOADS_DIR


class Utils:
    def __init__(self):
        pass

    def create_dir(self):
        os.makedirs(DOWNLOADS_DIR, exist_ok=True)
        os.makedirs(CAPTIONS_DIR, exist_ok=True)
        os.makedirs(VIDEOS_DIR, exist_ok=True)

    @staticmethod
    def get_vedio_id_from_url(url):
        return url.split('watch?v=')[-1]

    def get_caption_path(self, url):
        return os.path.join(CAPTIONS_DIR, self.get_vedio_id_from_url(url) + '.txt')

    def caption_file_exists(self, url):
        path = self.get_caption_path(url)
        return os.path.exists(path) and os.path.getsize(path) > 0

    def get_video_list_path(self, channel_id):
        return os.path.join(DOWNLOADS_DIR, channel_id + '_video_list.txt')

    def video_list_exists(self, channel_id):
        path = self.get_video_list_path(channel_id)
        return os.path.exists(path) and os.path.getsize(path) > 0