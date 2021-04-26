import time

from pytube import YouTube

from yt_concate.pipeline.steps.step import Step
from yt_concate.pipeline.steps.step import StepException


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()
        for url in data:
            print('Downloading caption for', url)
            if utils.caption_file_exists(url):
                continue
            try:
                source = YouTube(url)
                en_caption = source.captions.get_by_language_code('a.en')
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
                # print(en_caption_convert_to_srt)

            except (KeyError, AttributeError, FileNotFoundError, OSError) as e:
                print(e, 'when downloading caption for', url)
                continue
            text_file = open(utils.get_caption_path(url), "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()
        end = time.time()
        print('took', end-start, 'seconds')
