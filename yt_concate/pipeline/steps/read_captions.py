from .step import Step


class ReadCaptions(Step):
    def process(self, data, inputs, utils):
        for yt in data:
            if not utils.caption_file_exists(yt):
                continue
            with open(yt.caption_filepath, 'r') as c:
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
            yt.caption = captions
        return data
