import time

from pytube import YouTube

from yt_concate.pipeline.steps.step import Step
from yt_concate.pipeline.steps.step import StepException
from .get_video_list import GetVideoList


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        channel_id = inputs['channel_id']
        print(channel_id)
        start = time.time()
        error_list = [] # add error video list in order to don't take time to read again
        if utils.error_video_list_exists(channel_id):
            error_list = GetVideoList().read_file(utils.get_error_video_list_path(channel_id))

        for url in data:
            if utils.caption_file_exists(url):
                continue
            elif url in error_list:
                continue
            try:
                print('Downloading caption for', url)
                source = YouTube(url)
                en_caption = source.captions.get_by_language_code('a.en')
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
                # print(en_caption_convert_to_srt)

            except (KeyError, AttributeError, FileNotFoundError, OSError) as e:
                print(e, 'when downloading caption for', url)
                error_list.append(url)
                print(error_list)
                continue
            text_file = open(utils.get_caption_path(url), "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()
        GetVideoList().write_to_file(error_list, utils.get_error_video_list_path(channel_id))
        end = time.time()
        print('took', end - start, 'seconds')
