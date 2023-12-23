from urllib import parse as urlparser

from .base import BaseSpider

# CHINESE_DICT_URL = "https://www.mandarinspot.com/dict?word={}&phs=pinyin&sort=freq"
CHINESE_DICT_URL = "https://mandarinspot.com/dict?word={}&phs=pinyin&sort=freq?word={}&phs=pinyin&sort=freq"


class ChineseDictSpider(BaseSpider):
    name = "chinese_dict"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [
            CHINESE_DICT_URL.format(self.encode_vocab(word), self.encode_vocab(word))
            for word in self.ls_vocab
        ]
        self.max_sample = 10

    def extract_vocab(self, response):
        parsed_url = urlparser.urlparse(response.url)
        query_params = urlparser.parse_qs(parsed_url.query)
        vocab = query_params.get("word", [""])[0]
        return vocab

    def parse(self, response):
        word_rows = response.css("tr")
        count = 0
        ls_sample = []
        for row in word_rows:
            if count == 0:
                count += 1
                continue
            if count == self.max_sample:
                break
            word = row.css("td.hz a::text").extract_first()
            pinyin = row.css("td:nth-child(3)::text").extract_first()
            definition = row.css("td:nth-child(4)::text").extract_first()
            ls_sample.append({"word": word, "pinyin": pinyin, "definition": definition})
            count += 1
        vocab = self.extract_vocab(response)
        yield {"word": vocab, "sample": ls_sample}
