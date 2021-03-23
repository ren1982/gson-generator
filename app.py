from flask import Flask, render_template, url_for, redirect, request
# from pymarkovchain import MarkovChain
import requests
from flask_sqlalchemy import SQLAlchemy
import markovify
import random
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'] #"postgresql://gson:gson@localhost/gson"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# db.init_app(app)

from models import Lyrics
from utils import generate_lyric_segment, generate_chorus


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
    # Randomize verse size, chorus size, and title line number
    verse_length = random.randint(4, 8)
    chorus_length = random.randint(6, 10)
    title_line = random.randint(0, chorus_length-1)
    # Generate song segments
    verse_1 = generate_lyric_segment("VERSE", verse_length, text_model)
    verse_2 = generate_lyric_segment("VERSE", verse_length, text_model)
    bridge = generate_lyric_segment("BRIDGE", 4, text_model)
    chorus, title = generate_chorus(text_model, chorus_length, title_line)
    # Put together song
    generated_lyrics.extend(verse_1)
    generated_lyrics.extend(chorus)
    generated_lyrics.extend(verse_2)
    generated_lyrics.extend(chorus)
    generated_lyrics.extend(bridge)
    generated_lyrics.extend(chorus)
    lyrics = Lyrics(title=title, lyrics=generated_lyrics)
    db.session.add(lyrics)
    db.session.commit()
    url = lyrics.url
    return redirect(url_for('display_lyrics', url=url))


@app.route('/<url>')
def display_lyrics(url):
    lyrics_ = Lyrics.query.filter_by(url=url).first()
    if lyrics_:
        lyrics_.visits = lyrics_.visits + 1
        db.session.commit()
        return render_template('gson_generator/lyrics.html', lyrics=lyrics_)
    return redirect(url_for('main'))


@app.route('/explore')
@app.route('/explore/<order>')
def list_generated_lyrics(order='recent'):
    page = request.args.get('page', 1, type=int)
    if order == 'recent':
        listing = Lyrics.query.order_by(Lyrics.date_created.desc()).paginate(page=page, per_page=10)
    elif order == 'popular':
        listing = Lyrics.query.order_by(Lyrics.visits.desc()).paginate(page=page, per_page=10)
    else:
        return redirect(url_for('main'))
    return render_template('gson_generator/list.html', listing=listing, order=order)


if __name__ == '__main__':
    app.run(debug=True)
