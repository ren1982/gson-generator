from flask import Flask, render_template, url_for
# from pymarkovchain import MarkovChain
import requests
# from flask_sqlalchemy import SQLAlchemy
import markovify


app = Flask(__name__)
# db = SQLAlchemy()
# db.init_app(app)


@app.route('/')
def main():
    return render_template('gson_generator/main.html')

@app.route('/generate', methods=['POST'])
def generate_lyrics():
    lyrics_location = url_for('static', filename='lyrics.json', _external=True)
    response = requests.get(lyrics_location)
    lyric_list = response.json()
    lyrics = ''
    for lyric in lyric_list:
        lyrics += lyric['lyrics'].replace('...', '') + ' '
    # mc = MarkovChain()
    # mc.generateDatabase(lyrics)
    # generated_lyrics = []
    # for line in range(20):
    #     generated_lyrics.append(mc.generateString())
    text_model = markovify.NewlineText(lyrics, state_size=1)
    generated_lyrics = []
    title = text_model.make_sentence(tries=100, max_overlap_ratio=5)
    for i in range(24):
        generated_lyrics.append(text_model.make_sentence(tries=100, max_overlap_ratio=5))
    return render_template('gson_generator/lyrics.html', title=title, lyrics=generated_lyrics)



if __name__ == '__main__':
    app.run(debug=True)
