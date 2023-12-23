import os

from .base import BaseSpider

STROKE_URL = "https://www.strokeorder.com/assets/bishun/guide/{}.png"


class StrokeSpider(BaseSpider):
    name = "stroke"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [
            STROKE_URL.format(self.encode_vocab(word)) for word in self.ls_vocab
        ]
        self.save_dir = self.base_dir.joinpath("media/stroke")
        self.make_dir()

    def encode_vocab(self, word):
        return ord(word)

    def extract_vocab(self, response):
        keyword = os.path.basename(response.url).split(".")[0]
        vocab = chr(int(keyword))
        return vocab

    def parse(self, response):
        img_content = response.body
        vocab = self.extract_vocab(response)
        with open(f"{self.save_dir}/stroke_{vocab}.png", "wb") as f:
            f.write(img_content)
