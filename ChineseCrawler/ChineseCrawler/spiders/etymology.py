import os

from .base import BaseSpider

ETY_URL = "https://www.fantiz5.com/zi/ziyuantu/{}.png"


class EtymologySpider(BaseSpider):
    name = "etymology"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [
            ETY_URL.format(self.encode_vocab(word)) for word in self.ls_vocab
        ]
        # self.base_dir + "media/etymology/"
        self.save_dir = self.base_dir.joinpath("media/etymology")
        self.make_dir()

    def encode_vocab(self, word):
        return word.encode("utf-8").hex()

    def extract_vocab(self, response):
        keyword = os.path.basename(response.url).split(".")[0]
        vocab = bytes.fromhex(keyword).decode("utf-8")
        return vocab

    def parse(self, response):
        img_content = response.body
        vocab = self.extract_vocab(response)
        with open(f"{self.save_dir}/ety_{vocab}.png", "wb") as f:
            f.write(img_content)
