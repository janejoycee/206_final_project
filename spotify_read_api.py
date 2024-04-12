import spotipy
# from billboard_read_api import get_artist_list


from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

def spotify_artist_information(date):
    scope = "user-library-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    cl_id = 'e6b2e0e41e54431c9819db2c2694a261'
    secret_id = '515d03cc40d64571a328d13d27afb079'
    client_credentials_manager = SpotifyClientCredentials(client_id=cl_id, client_secret=secret_id)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

    # list_of_top_artists = get_artist_list(date)

    artist = "Ed Sheeran"
    results = sp.search(q=artist, limit=1, type='artist')

    print(results)
    # for artist in list_of_top_artists:
    #     results = sp.search(q=artist, limit=1, type='artist')


spotify_artist_information('2023-05-01')

