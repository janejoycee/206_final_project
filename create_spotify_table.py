import sqlite3
from spotify_read_api import spotify_artist_information

artist_info = spotify_artist_information('2023-05-01')


# def create_spotify_table(cur, conn, start_id):
#     cur.execute("CREATE TABLE IF NOT EXISTS Spotify (spotify_artist_id INTEGER PRIMARY KEY, spotify_artist_name TEXT, follower_count INTEGER)")
#     for i in range(start_id, start_id + 25):
#         if i < len(artist_info):
#             artist = list(artist_info.keys())[i]
#             follower_count = artist_info[artist]['followers']
#             cur.execute("INSERT OR IGNORE INTO Spotify (spotify_artist_id, spotify_artist_name, follower_count) VALUES (?, ?, ?)",
#                         (i, artist, follower_count))
#     conn.commit()

def add_spotify_info(cur, conn, start_id):
    cur.execute("CREATE TABLE IF NOT EXISTS Spotify_followers (spotify_artist_id INTEGER PRIMARY KEY, follower_count INTEGER)")
    for i in range(start_id, start_id + 25):
        if i < len(artist_info):
            artist = list(artist_info.keys())[i]
            follower_count = artist_info[artist]['followers']
            cur.execute("INSERT OR IGNORE INTO Spotify_followers (spotify_artist_id, follower_count) VALUES (?, ?)",
                        (i, follower_count))
    conn.commit()

def create_spotify_popularity_table(cur, conn, start_id):
    cur.execute("CREATE TABLE IF NOT EXISTS Spotify_popularity (spotify_artist_id INTEGER PRIMARY KEY, popularity_index INTEGER)")
    for i in range(start_id, start_id + 25):
        if i < len(artist_info):
            artist = list(artist_info.keys())[i]
            popularity_index = artist_info[artist]['popularity']
            cur.execute("INSERT OR IGNORE INTO Spotify_popularity (spotify_artist_id, popularity_index) VALUES (?, ?)",
                        (i,popularity_index))
    conn.commit()


def update_start_id(start_id):
    with open('spotify_start_id.txt', 'w') as file:
        file.write(str(start_id))

def get_start_id():
    with open('spotify_start_id.txt', 'r') as file:
        return int(file.readline())


def main():
    conn = sqlite3.connect("artist.db")
    cur = conn.cursor()
    start_id = get_start_id()
    # create_spotify_table(cur, conn, start_id)
    add_spotify_info(cur, conn, start_id)
    create_spotify_popularity_table(cur, conn, start_id)
  

    update_start_id(start_id + 25)

    conn.close()

if __name__ == "__main__":
    main()