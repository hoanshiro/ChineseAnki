from ..items import HanziiSpiderItem
from .base import BaseSpider

HANZII_URL = "https://api.hanzii.net/api/search/vi/{}?type=word&page=1&limit=2"


class HanziiSpider(BaseSpider):
    name = "hanzii"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [
            HANZII_URL.format(self.encode_vocab(word), self.encode_vocab(word))
            for word in self.ls_vocab
        ]

    def parse(self, response):
        try:
            response_json = response.json()
            vocab_data = response_json["result"][0]
        except:
            return
        item = HanziiSpiderItem()
        item["word"] = vocab_data["word"]
        item["pinyin"] = vocab_data["pinyin"]
        item["cn_vi"] = vocab_data["cn_vi"]
        item["compound"] = self.get_compound(vocab_data)
        num_def = 3
        ls_defs = vocab_data["content"][0]["means"]
        for idx, def_data in enumerate(ls_defs[:num_def]):
            item[f"def_{idx+1}"] = f"{def_data['explain']}: {def_data['mean']}"
            if not (examples_data := def_data.get("examples")):
                continue
            ex_1st = examples_data[0]
            item[f"ex_{idx+1}"] = f"{ex_1st['e']} - {ex_1st['p']} - {ex_1st['m']}"
        yield item

    @staticmethod
    def get_compound(vocab_data):
        ls_compound = (vocab_data.get("compound") or "").split(" ; ")
        num_compound = 10 if len(ls_compound) > 10 else len(ls_compound)
        compound = " ; ".join(ls_compound[:num_compound])
        return compound
