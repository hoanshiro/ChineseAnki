from genanki import Model, Note
import genanki

CSS = '''
    .card {
        font-family: Segoe UI;
        font-size: 20px;
        text-align: left;
        color: black;
        background-color: white;
    }
    .image-container {
        display: flex;
        justify-content: space-between;
    }
    img{
        max-width:100%;

        height:auto;
            width:300px;
            border-radius: 20px;
    }
'''

TEMPLATE = [{
    'name': 'Anki Card (Improved Format)',
    'qfmt': '''
        <center><h1>{{word}} - {{pinyin}} - {{word_mp3}}</h1></center><hr>
        <b>Definition:</b> {{definition}}<br>
        <lef> <b>Example 1:</b> {{ex1}} - {{ex1_def}} - {{ex1_mp3}}</left><hr>
        <hr id="answer">
        <lef> <b>Example 2:</b> {{ex2}} - {{ex2_def}} - {{ex2_mp3}}</left><hr>
        <lef> <b>Example 3:</b> {{ex3}} - {{ex3_def}} - {{ex3_mp3}}</left><hr>
        <lef> <b>Example 4:</b> {{ex4}} - {{ex4_def}} - {{ex4_mp3}}</left><hr>
        <lef> <b>Example 5:</b> {{ex5}} - {{ex5_def}} - {{ex5_mp3}}</left><hr>
    ''',
    'afmt': '''
        {{FrontSide}}
        <hr id="answer">
        '<div style="text-align: left;">{{etymology}}<br><img src="{{stroke_order}}" style="width: 200px; height: 200px;"></div><br>'
        <lef> <b>Example 6:</b> {{ex6}} - {{ex6_def}} - {{ex6_mp3}}</left><hr>
        <lef> <b>Example 7:</b> {{ex7}} - {{ex7_def}} - {{ex7_mp3}}</left><hr>
        <lef> <b>Example 8:</b> {{ex8}} - {{ex8_def}} - {{ex8_mp3}}</left><hr>
        <lef> <b>Example 9:</b> {{ex9}} - {{ex9_def}} - {{ex9_mp3}}</left><hr>
    ''',
}]

class AnkiGener:
    def __init__(self):
        '''
        repo: https://github.com/kerrickstaley/genanki
        '''
        self.css = CSS
        self.card_template = TEMPLATE

    def create_card(self, fields):
        my_model = Model(
            1607392319,
            'Anki Card Model',
            fields=fields,
            templates=self.card_template,
            css=self.css,
        )
        return my_model
    
    def create_desktop_deck(self, deck_name, model, notes):
        my_deck = genanki.Deck(
            2059400110,
            deck_name,
        )
        for note in notes:
            my_deck.add_note(note)
        return my_deck
    
    def import_media(self, deck, media_files):
        for file in media_files:
            deck.media_files.append(file)
        return deck
    
    def export_deck(self, deck, file_name):
        genanki.Package(deck).write_to_file(file_name)
        return True
    
    def execute(self, deck_name, fields, notes, media_files, file_name):
        model = self.create_card(fields)
        deck = self.create_desktop_deck(deck_name, model, notes)
        deck = self.import_media(deck, media_files)
        self.export_deck(deck, file_name)
        return True