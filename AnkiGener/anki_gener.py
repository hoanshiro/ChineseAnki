from genanki import Model, CLOZE_MODEL
import genanki
import os
from template import TEMPLATE, CSS, FIELDS, KEY_ORDER
from field_parser import FieldParser

class AnkiGener:
    def __init__(self, data_path, media_path):
        '''
        repo: https://github.com/kerrickstaley/genanki
        '''
        self.css = CSS
        self.card_template = TEMPLATE
        self.fields = FIELDS
        self.chinse_model = self.create_model()
        self.data_path = data_path
        self.media_path = media_path
        self.field_parser = FieldParser(self.data_path)
        self.data = self.field_parser.parse()

    def create_model(self):
        chinse_model = Model(
            1607392319,
            'Chinese Card Model',
            model_type=Model.CLOZE,
            fields=self.fields,
            templates=self.card_template,
            css=self.css,
        )
        return chinse_model
    

    def create_deck(self, deck_name):
        chinse_desk = genanki.Deck(
            2059400110,
            deck_name,
        )
        for item in self.data:
            card = genanki.Note(
                model=self.chinse_model,
                fields=[item[key] for key in KEY_ORDER],
            )
            chinse_desk.add_note(card)
        return chinse_desk

    def create_package(self, deck, media_files):
        chinese_package = genanki.Package(deck)
        for file in media_files:
            chinese_package.media_files.append(file)
        chinese_package.write_to_file('Chinese.apkg')
        return True

    def create_media_files(self):
        sub_folders = ['audio', 'etymology', 'stroke', 'hanzii_audio']
        media_files = []
        for folder in sub_folders:
            folder_path = f'{self.media_path}/{folder}'
            for file in os.listdir(folder_path):
                media_files.append(f'{folder_path}/{file}')
        print("Number of media files: ", len(media_files))
        return media_files

    def execute(self, deck_name):
        deck = self.create_deck(deck_name)
        media_files = self.create_media_files()
        is_sucess = self.create_package(deck, media_files)
        return is_sucess

if __name__ == '__main__':
    data_path = '/home/hoan/Desktop/ChineseAnki/ChineseCrawler/hanzii.json'
    media_path = '/home/hoan/Desktop/ChineseAnki/ChineseCrawler/ChineseCrawler/media'
    anki_gener = AnkiGener(data_path, media_path)
    anki_gener.execute('ChineseHanzii')