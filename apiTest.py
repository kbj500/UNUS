import spotipy
from spotipy.oauth2 import SpotifyOAuth
"""
SPOTIPY_CLIENT_ID='63b042243c2548b5b3ebb02756e84cb4'
SPOTIPY_CLIENT_SECRET='96bc8bc908894f9ab922ac0f0d52127a'"""
spotipy.SpotifyClientCredentials()
scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])