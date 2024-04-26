import sqlite3
from billboard_read_api import get_artist_list
from grammy import retrieve_listings

def create_grammy_billboard_table(cur, conn, start_id):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Grammy_billboard_artists (
            billboard_artist_name TEXT,
            nominations_num INTEGER)
        """)
    category_dict = retrieve_listings()
    artist_list = get_artist_list("2023-05-01")
    print(artist_list)
    artist_nominations = {}
    
    for category, nominees in category_dict.items():
        for nominee in nominees:
            artist_name = nominee.split(" — ")[-1]
            if artist_name in artist_nominations:
                artist_nominations[artist_name] += 1
            else:
                artist_nominations[artist_name] = 1
    print((list(artist_nominations.items()))[0:6])

    for i in range(start_id, start_id + 25):
        if i < len(artist_list):
            artist = artist_list[i]
            cur.execute("""INSERT OR IGNORE INTO Grammy_billboard_artists 
                            (billboard_artist_name, nominations_num) 
                            VALUES (?, ?)""", (artist, artist_nominations.get(artist_list[i], 0)))   
    conn.commit()

    # conn.commit()
 
def update_start_id(start_id):
    with open('billboard_grammy_start_id.txt', 'w') as file:
        file.write(str(start_id))

def get_start_id():
    with open('billboard_grammy_start_id.txt', 'r') as file:
        return int(file.readline())


def main():
    conn = sqlite3.connect('artist.db')
    cur = conn.cursor()
    start_id = get_start_id()
    create_grammy_billboard_table(cur, conn, start_id)
    update_start_id(start_id + 25)

    conn.close()

if __name__ == "__main__":
     main()
