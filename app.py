from flask import Flask, render_template, url_for, redirect
# from pymarkovchain import MarkovChain
import requests
from flask_sqlalchemy import SQLAlchemy
import markovify
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'] #"postgresql://gson:gson@localhost/gson"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# db.init_app(app)

from models import Lyrics


@app.route('/')
def main():
    return render_template('gson_generator/main.html')


@app.route('/generate', methods=['POST'])
def generate_lyrics():
    lyrics_location = url_for('static', filename='lyrics.json', _external=True)
    response = requests.get(lyrics_location)
    lyric_list = response.json()
    lyric_text = ''
    for lyric in lyric_list:
        lyric_text += lyric['lyrics'].replace('...', '') + ' '
    text_model = markovify.NewlineText(lyric_text, state_size=1)
    generated_lyrics = []
    title = text_model.make_sentence(tries=100, max_overlap_ratio=5)
    for i in range(24):
        generated_lyrics.append(text_model.make_sentence(tries=100, max_overlap_ratio=5))
    lyrics = Lyrics(title=title, lyrics=generated_lyrics)
    db.session.add(lyrics)
    db.session.commit()
    url = lyrics.url
    return redirect(url_for('display_lyrics', url=url))


@app.route('/<url>')
def display_lyrics(url):
    lyrics = Lyrics.query.filter_by(url=url).first()
    title = lyrics.title
    lyrics = lyrics.lyrics
    return render_template('gson_generator/lyrics.html', title=title, lyrics=lyrics, url=url)


if __name__ == '__main__':
    app.run(debug=True)
