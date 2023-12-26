from ..items import HanziiSpiderItem
from scrapy import Request
import json
import jmespath
from .base import BaseSpider

HANZII_URL = "https://api.hanzii.net/api/search/vi/{}?type=word&page=1&limit=2"
KANJI_URL = "https://api.hanzii.net/api/search/vi/{}?type=kanji&page=1&limit=1"
HANZII_AUDIO_URL = "https://audio.hanzii.net/audios/e_cnvi/{gender}/{id}.mp3"


class HanziiSpider(BaseSpider):
    name = "hanzii"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [
            HANZII_URL.format(self.encode_vocab(word), self.encode_vocab(word))
            for word in self.ls_vocab
        ]
        self.kanji = self.load_kanji(
            kanji_path=f"{self.base_dir}/data/kanji.json"
        )
        self.save_dir = self.base_dir.joinpath("media/hanzii_audio")
        self.make_dir()

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
        # search from ls_defs
        ls_backup_examples = jmespath.search("[*].examples[*]", ls_defs)
        breakpoint()
        for idx, def_data in enumerate(ls_defs[:num_def]):
            item[f"def_{idx+1}"] = f"{def_data['explain']}: {def_data['mean']}"
            if not (examples_data := def_data.get("examples")):
                ex_1st = examples_data[0]
            else:
                try:
                    ex_1st = ls_backup_examples[0][0]
                    ls_backup_examples.pop(0)
                except Exception:
                    continue
            item[f"ex_{idx+1}"] = f"{ex_1st['e']} - {ex_1st['p']} - {ex_1st['m']}"
            audio_idx = ex_1st["id"]
            random_gender = "1" if audio_idx % 2 == 0 else "0"
            save_path = self.save_dir.joinpath(f'audio_{ex_1st["e"]}.mp3')
            if save_path.exists():
                continue
            yield Request(
                HANZII_AUDIO_URL.format(gender=random_gender, id=audio_idx),
                callback=self.parse_audio,
                cb_kwargs=dict(meta=ex_1st["e"]),
            )
        self.item = item
        yield Request(
            url=KANJI_URL.format(self.encode_vocab(item["word"])),
            callback=self.parse_kanji,
            cb_kwargs=dict(item=item),
            errback=self.errback,
        )

    def parse_audio(self, response, meta):
        name = meta
        with open(f"{self.save_dir}/audio_{name}.mp3", "wb") as f:
            f.write(response.body)


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
