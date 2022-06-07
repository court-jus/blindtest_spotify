import spotipy
import time
from pprint import pprint
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

scope = "user-library-read,user-modify-playback-state,user-read-playback-state,user-read-currently-playing"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope=scope,
    client_id="fillme",
    client_secret="fillme",
    redirect_uri="fillme",
))

pl_id = 'spotify:playlist:6lJ6ld9gPVuFgDHDZQxCkK'
offset = 0

def get_followers(track):
    urn = "spotify:artist:" + track["artists"][0]["id"]
    artist = sp.artist(urn)
    return artist.get("followers", {}).get("total", 0)

def print_track_info(track):
    print(";".join([track["name"], track["external_urls"]["spotify"], track["artists"][0]["name"], str(get_followers(track)), str(track["popularity"])]))

popularities = []
followers = []
while True:
    response = sp.playlist_items(pl_id,
                                 offset=offset,
                                 fields='items.track.id,total',
                                 additional_types=['track'])
    
    if len(response['items']) == 0:
        break
    for item in response["items"]:
        urn = "spotify:track:" + item["track"]["id"]
        track = sp.track(urn)
        print_track_info(track)
    offset = offset + len(response['items'])

current = None
while False:
    playback = sp.current_playback()
    track = playback["item"]
    if current is None or track["id"] != current:
        print_track_info(track)
        current = track["id"]
    time.sleep(10)