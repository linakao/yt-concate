import time

from pytube import YouTube

from yt_concate.pipeline.steps.step import Step
from yt_concate.pipeline.steps.step import StepException



class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        channel_id = inputs['channel_id']
        print(channel_id)
        start = time.time()
        error_list = [] # add error video list in order to don't take time to read again
        if utils.error_video_list_exists(channel_id):
            error_list = utils.read_file(utils.get_error_video_list_path(channel_id))

        for yt in data:
            if utils.caption_file_exists(yt):
                continue
            elif yt.url in error_list:
                continue
            try:
                print('Downloading caption for', yt.url)
                source = YouTube(yt.url)
                en_caption = source.captions.get_by_language_code('a.en')
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
                # print(en_caption_convert_to_srt)

            except (KeyError, AttributeError, FileNotFoundError, OSError) as e:
                print(e, 'when downloading caption for', yt.url)
                error_list.append(yt.url)
                continue
            text_file = open(yt.caption_filepath, "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()
        utils.write_to_file(error_list, utils.get_error_video_list_path(channel_id))
        end = time.time()
        print('downloading captions took', end - start, 'seconds')
        return data
