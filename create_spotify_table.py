import sqlite3


def create_spotify_table(cur, conn, start_id):
    limit = 25
    cur.execute("CREATE TABLE IF NOT EXISTS Spotify (spotify_artist_id INTEGER PRIMARY KEY, spotify_artist_name TEXT, follower_count TEXT, pop_index TEXT)")
    for i in range(start_id, start_id + 25):
        if i < 100:
            cur.execute("""
            INSERT OR IGNORE INTO Spotify (spotify_artist_id, spotify_artist_name)
            SELECT identification, name
            FROM Artist
            """)
    conn.commit()

def update_start_id(start_id):
    with open('spotify_start_id.txt', 'w') as file:
        file.write(str(start_id))

def get_start_id():
    with open('spotify_start_id.txt', 'r') as file:
        return int(file.readline())

# def create_spotify_table(cur, conn, start_id):
#     limit = 25
#     cur.execute("CREATE TABLE IF NOT EXISTS Spotify (spotify_artist_id INTEGER PRIMARY KEY, spotify_artist_name TEXT, follower_count TEXT, pop_index TEXT)")

#     for i in range(start_id, start_id + limit):
#         if i < len(artist_list):
#             cur.execute("INSERT INTO Artist (identification, name) VALUES (?, ?)",
#                         (i, artist_list[i]))
#     conn.commit()

# def update_start_id(start_id):
#     with open('start_id.txt', 'w') as file:
#         file.write(str(start_id))

# def get_start_id():
#     with open('spotify_start_id.txt', 'r') as file:
#         return int(file.readline())

def main():
    conn = sqlite3.connect('artist.db')
    cur = conn.cursor()
    start_id = get_start_id()
    create_spotify_table(cur, conn, start_id)
  

    update_start_id(start_id + 25)

    conn.close()

if __name__ == "__main__":
    main()