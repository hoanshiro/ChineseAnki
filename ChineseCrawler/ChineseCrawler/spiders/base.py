import json
from pathlib import Path

import scrapy


class BaseSpider(scrapy.Spider):
    name = "base"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_dir = Path(__file__).resolve().parent
        self.base_dir = self.file_dir.parent
        self.vocab_path = f"{self.base_dir}/data/vocab.json"
        self.save_dir = ""
        self.ls_vocab = self.load_vocab()

    def make_dir(self):
        if self.save_dir:
            Path(self.save_dir).mkdir(parents=True, exist_ok=True)

    def load_vocab(self):
        with open(self.vocab_path) as f:
            dict_vocab = json.load(f)
        ls_vocab = []
        for key in dict_vocab:
            #  "HSK1": "的 一 是 在 了 有 人 不 国
            current_vocab = dict_vocab[key].split(" ")
            ls_vocab.extend(current_vocab)
        return ls_vocab

    def encode_vocab(self, word):
        return word

    def extract_vocab(self, response):
        return response.url.split("/")[-1].split(".")[0]

    @staticmethod
    def combine_items(data: list, delimiter=", "):
        return delimiter.join(filter(None, data))
