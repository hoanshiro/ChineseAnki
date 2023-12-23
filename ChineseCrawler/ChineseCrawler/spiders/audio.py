from pypinyin import Style, pinyin
from scrapy.http import Request

from .base import BaseSpider

AUDIO_URL = "https://dictionary.writtenchinese.com/sounds/{}.mp3"


class AudioSpider(BaseSpider):
    name = "audio"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [AUDIO_URL]
        self.save_dir = self.base_dir.joinpath("media/audio")
        self.make_dir()

    def start_requests(self):
        for vocab in self.ls_vocab:
            url = AUDIO_URL.format(self.encode_vocab(vocab))
            yield Request(url, dont_filter=True, meta={"vocab": vocab})

    def encode_vocab(self, word):
        keyword = pinyin(word, style=Style.TONE3, heteronym=True)[0][0]
        if not keyword[-1].isdigit():
            keyword += "5"
        return keyword

    def extract_vocab(self, response):
        vocab = response.meta["vocab"]
        return vocab

    def parse(self, response):
        img_content = response.body
        vocab = self.extract_vocab(response)
        with open(f"{self.save_dir}/audio_{vocab}.mp3", "wb") as f:
            f.write(img_content)
