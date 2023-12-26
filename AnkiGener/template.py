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

TEMPLATE = [
    {
        'name': 'Anki Card (Improved Format)',
        'qfmt': '''
        <center><h1>{{cloze:word}} - {{pinyin}} - {{word_mp3}}</h1></center><hr>
        <b>Definition 1:</b> {{def_1}}<hr>
        <b>Example 1: </b> {{cloze::ex_1}} - {{ex_1_mp3}}<hr>
        <div style='font-family: Segoe UI;text-align:center;'>{{type::word}}
    ''',
        'afmt': '''
        {{FrontSide}}
        <hr id="answer">
        <center><h1>{{cloze:word}}<h1></center><hr>
        <div style="text-align: center;">{{etymology}} {{stroke_order}}</div><hr>
        <div style="text-align: left;">
            <b>Definition 2:</b> {{def_2}}<br>
            <b>Example 2: </b> {{ex_2}} - {{ex_2_mp3}}<hr>
            <b>Definition 3:</b> {{def_3}}<br>
            <b>Example 3: </b> {{ex_3}} - {{ex_3_mp3}}<hr>
            <b>Composition: </b> {{comp}}<hr>
            <b>Super Composition: </b> {{scomp}}<hr>
            <b>Compound: </b> {{compound}}<hr>
        </div>
    ''',
    }
]
KEY_ORDER = ['word', 'pinyin', 'cn_vi', 'def_1', 'ex_1', 'def_2', 'ex_2',
             'def_3', 'ex_3', 'comp', 'scomp', 'compound', 'etymology',
             'stroke_order', 'word_mp3', 'ex_1_mp3', 'ex_2_mp3', 'ex_3_mp3']
FIELDS = [{'name': key} for key in KEY_ORDER]