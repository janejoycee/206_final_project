import spotipy
import json
from billboard_read_api import get_artist_list
from spotipy.oauth2 import SpotifyClientCredentials

def spotify_artist_information(date):

    client_id = 'e6b2e0e41e54431c9819db2c2694a261'
    secret_id = '515d03cc40d64571a328d13d27afb079'
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=secret_id)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


    artist_popularity_dict = {}
    list_of_top_artists = get_artist_list(date)

    for artist in list_of_top_artists:
        results = sp.search(q=artist, limit=1, type='artist')
        followers = results['artists']['items'][0]['followers']['total']
        popularity_index = results['artists']['items'][0]['popularity']
        if artist not in artist_popularity_dict:
            artist_popularity_dict[artist] = {'followers': followers, 'popularity': popularity_index}
    print(artist_popularity_dict)
    return artist_popularity_dict
        




spotify_artist_information('2023-05-01')


