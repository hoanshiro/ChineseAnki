import json
from template import KEY_ORDER
from tqdm import tqdm

class FieldParser:
    def __init__(self, data_path):
        self.data = self.load_json(data_path)

    def parse(self):
        '''
        {
            "word":"拧",
            "pinyin":"nǐng",
            "cn_vi":"ninh",
            "compound":"",
            "def_1":"控制住物体向里转或向外转: vặn",
            "ex_1":"拧螺丝。 - nǐng luósī。 - vặn ốc.",
            "def_2":"颠倒;错: sai; lộn; lẫn lộn; nhầm",
            "ex_2":"他想说'狗嘴里长不出象牙'。 - tā xiǎng shuō ' gǒuzǔilǐ chángbùchū xiàngyá '。 - anh ấy muốn nói 'miệng chó thì không thể nào mọc ra ngà voi'",
            "def_3":"别扭;抵触: gay gắt; mâu thuẫn",
            "ex_3":"两个人越说越拧。 - liǎnggè rényuè shuō yuè nǐng。 - hai người càng nói càng gay gắt.",
            "comp":"宁: NINH, 扌: THỦ",
            "scomp":""
        }
        '''
        for item in tqdm(self.data):
            # breakpoint()
            item['etymology'] = f'<img src="ety_{item["word"]}.png">'
            item['stroke_order'] = f'<img src="stroke_{item["word"]}.png">'
            item['word_mp3'] = f'[sound:audio_{item["word"]}.mp3]'
            for key in KEY_ORDER:
                item[key] = item[key] if item.get(key) else ''
            cloze_word = self.add_cloze(item['word'])
            item['ex_1_mp3'] = self.create_sound_field(item, 'ex_1')
            item['ex_2_mp3'] = self.create_sound_field(item, 'ex_2')
            item['ex_3_mp3'] = self.create_sound_field(item, 'ex_3')
            item['ex_1'] = item['ex_1'].replace(item['word'], cloze_word)
        return self.data
    
    @staticmethod
    def add_cloze(value):
        value = '{{c1::' + value + '}}'
        return value

    @staticmethod
    def create_sound_field(item, key):
        if example := item.get(key):
            chinese_part = example.split(' - ')[0]
            return f'[sound:audio_{chinese_part}.mp3]'
        return ''
        

    def load_json(self, data_path):
        with open(data_path, 'r') as f:
            data = json.load(f)        
            return data

if __name__ == '__main__':
    parser = FieldParser('/home/hoan/Desktop/ChineseAnki/ChineseCrawler/hanzii.json')
    parser.parse()
    print(json.dumps(parser.data[0], indent=4, ensure_ascii=False))