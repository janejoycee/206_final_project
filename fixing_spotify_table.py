import sqlite3

def remove_columns_from_spotify_table(conn, cur):

    cur.execute('''UPDATE Spotify 
                SET follower_count = (SELECT f.follower_count FROM Spotify_followers AS f WHERE Spotify.spotify_artist_id = f.spotify_artist_id),
                    pop_index = (SELECT p.popularity_index FROM Spotify_popularity AS p WHERE Spotify.spotify_artist_id = p.spotify_artist_id)
                WHERE Spotify.spotify_artist_id BETWEEN 0 AND 99''')

    conn.commit()



def main():
    conn = sqlite3.connect('artist.db')
    cur = conn.cursor()
    remove_columns_from_spotify_table(conn, cur)
    conn.close()


if __name__ == "__main__":
    main()