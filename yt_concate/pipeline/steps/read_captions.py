import os
from pprint import pprint

from .step import Step
from yt_concate.settings import CAPTIONS_DIR


class ReadCaptions(Step):
    def process(self, data, inputs, utils):
        data = {}
        for caption_file in os.listdir(CAPTIONS_DIR):
            with open(os.path.join(CAPTIONS_DIR, caption_file), 'r') as c:
                time_line = False
                time = None
                captions = {}
                for line in c:
                    if '-->' in line:
                        time_line = True
                        time = line.strip()
                    elif time_line:
                        caption = line.strip()
                        captions[caption] = time
                        time_line = False
                    else:
                        continue
            data[caption_file] = captions
        pprint(data)
        return data

