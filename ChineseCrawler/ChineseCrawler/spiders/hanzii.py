from ..items import HanziiSpiderItem
from scrapy import Request
import json
from .base import BaseSpider

HANZII_URL = "https://api.hanzii.net/api/search/vi/{}?type=word&page=1&limit=2"
KANJI_URL = "https://api.hanzii.net/api/search/vi/{}?type=kanji&page=1&limit=1"


class HanziiSpider(BaseSpider):
    name = "hanzii"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [
            HANZII_URL.format(self.encode_vocab(word), self.encode_vocab(word))
            for word in self.ls_vocab
        ]
        self.kanji = self.load_kanji(
            kanji_path="/Users/nguyenvanhoan/Anki/ChineseAnki/ChineseCrawler/kanji.json"
        )

    def load_kanji(self, kanji_path):
        with open(kanji_path) as f:
            kanji = json.load(f)
        return kanji

    def parse(self, response):
        try:
            response_json = response.json()
            vocab_data = response_json["result"][0]
        except Exception:
            return None
        item = HanziiSpiderItem()
        item["word"] = vocab_data["word"]
        item["pinyin"] = vocab_data["pinyin"]
        item["cn_vi"] = vocab_data["cn_vi"]
        ls_compound = (vocab_data.get("compound") or "").split(" ; ")
        item["compound"] = self.get_compound(ls_compound)
        num_def = 3
        ls_defs = vocab_data["content"][0]["means"]
        for idx, def_data in enumerate(ls_defs[:num_def]):
            item[f"def_{idx+1}"] = f"{def_data['explain']}: {def_data['mean']}"
            if not (examples_data := def_data.get("examples")):
                continue
            ex_1st = examples_data[0]
            item[f"ex_{idx+1}"] = f"{ex_1st['e']} - {ex_1st['p']} - {ex_1st['m']}"
        self.item = item
        yield Request(
            url=KANJI_URL.format(self.encode_vocab(item["word"])),
            callback=self.parse_kanji,
            cb_kwargs=dict(item=item),
            errback=self.errback,
        )

    def parse_kanji(self, response, item):
        try:
            response_json = response.json()
            vocab_data = response_json["result"][0]
        except Exception:
            return None
        detail_data = vocab_data["detail"]
        comp = [
            f"{kanji}: {self.kanji.get(kanji) or ''}" for kanji in detail_data["comp"]
        ]
        scomp = [
            f"{kanji}: {self.kanji.get(kanji) or ''}" for kanji in detail_data["scomp"]
        ]
        item["comp"] = self.get_compound(comp)
        item["scomp"] = self.get_compound(scomp)
        yield item

    def errback(self):
        yield self.item

    def get_compound(self, ls_compound):
        num_compound = 10 if len(ls_compound) > 10 else len(ls_compound)
        compound = self.combine_items(ls_compound[:num_compound])
        return compound
