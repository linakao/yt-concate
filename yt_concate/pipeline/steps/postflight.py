from .step import Step


class Postflight(Step):
    def process(self, data, inputs, utils):
        print('in postflight')
        utils.create_dir()
