import spotipy
from decouple import config
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read"
client_id=config('SPOTIPY_CLIENT_ID')
client_secret=config('SPOTIPY_CLIENT_SECRET')
redirect_uri=config('SPOTIPY_REDIRECT_URI')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id,
                     client_secret=client_secret, redirect_uri=redirect_uri))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])

print(results.keys())