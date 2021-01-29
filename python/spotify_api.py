import spotipy
import sys
import random
from decouple import config
from spotipy.oauth2 import SpotifyOAuth
import json

# Scope allows for different permisions as to what the API can access https://developer.spotify.com/documentation/general/guides/scopes/#streaming 
# Scope uses split() method on string so you can just add scopes to a single string with a space between them for multiple scopes
scope = "user-library-read user-read-currently-playing user-modify-playback-state"
client_id=config('SPOTIPY_CLIENT_ID')
client_secret=config('SPOTIPY_CLIENT_SECRET')
redirect_uri=config('SPOTIPY_REDIRECT_URI')

# Instantiating Spotify API object and passing appropriate perameters 
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id,
                     client_secret=client_secret, redirect_uri=redirect_uri))

def get_saved_list():
    '''Retreive current top 20 saved songs and print arist and song name'''
    results = sp.current_user_saved_tracks()
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])

def get_current_song():
    '''Retreive current playing song and printing the artist and song name'''
    results = sp.current_user_playing_track()
    track = results['item']
    print(track['artists'][0]['name'], ' - ', f"'{track['name']}'")

def set_song_random():
    '''Sets current playback song to a random song from saved list(top 20)'''
    uri = get_random_song()
    sp.add_to_queue(uri=uri)
    sp.next_track()

def get_random_song():
    '''Returns random song ID from top 20 recent saved songs'''
    results = sp.current_user_saved_tracks()
    song_id = results['items'][random.randint(0,19)]['track']['id']
    return song_id

def current_track_time():
    ''' Returns tuple (progress_ms, duration_ms) of current track '''
    results = sp.current_user_playing_track()
    with open('song_data.json', 'w') as file:
        json.dump(results, file, indent=4)
    return (results['progress_ms'], results['item']['duration_ms'])

def ms_to_time(ms):
    ''' Convers ms to (minute:seconds) fromat as str '''
    total_seconds = ms//1000
    minutes = total_seconds//60
    seconds = total_seconds % 60
    return f'{minutes}:{seconds}'

def seek_back(seconds=10):
    '''' Seek will go back the an amount of seconds based on "seconds" parameter'''
    seconds_in_ms = seconds * 1000
    ms = current_track_time()[0] - seconds_in_ms
    sp.seek_track(ms)

if __name__ == '__main__':
    globals()[sys.argv[1]]()