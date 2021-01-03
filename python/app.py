from flask import Flask
from .spotify_api import set_song_random

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, world!'

@app.route('/random')
def random_song():
    set_song_random()
    return 'You are now listening to a random song from your saved list'