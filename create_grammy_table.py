import sqlite3
import grammy
from billboard_read_api import get_artist_list

listing_data = grammy.retrieve_listings()
winners_data = grammy.get_winners()


conn = sqlite3.connect('artist.db')
cur = conn.cursor()

def create_grammy_table(cur, conn, artist_list, start_id):


    limit = 25
    cur.execute("CREATE TABLE IF NOT EXISTS Grammy (grammy_artist_id INTEGER PRIMARY KEY, grammy_artist_name TEXT, nominations TEXT, winning_awards TEXT)")

    for i in range(start_id, start_id + limit):
        if i < len(artist_list):
            cur.execute("INSERT INTO Grammy (grammy_artist_id, grammy_artist_name) VALUES (?, ?)",
                        (i, artist_list[i]))
    conn.commit()

def update_start_id(start_id):
    with open('grammy_start_id.txt', 'w') as file:
        file.write(str(start_id))

def get_start_id():
    with open('grammy_start_id.txt', 'r') as file:
        return int(file.readline())
    
def insert_grammy_data(cur, conn, listing_data, winners_data, artist_list):
    for award, nominees in listing_data.items(): 
        for nominee in nominees:
            #print(nominee)

            #artist_name = nominee.split('—')[1].strip()  # Assuming the artist name follows the pattern "Song Title — Artist Name"

            cur.execute("""
            SELECT * FROM Grammy WHERE grammy_artist_name = ?
            """, (nominee,))
            existing_record = cur.fetchone()

            if existing_record:
    
                cur.execute("""
                UPDATE Grammy SET nominations = nominations || ', ' || ? WHERE grammy_artist_name = ?
                """, (award, nominee))
            else:
                continue

    for award, winner in winners_data.items():
        cur.execute("""
        UPDATE Grammy
        SET winning_awards = ?
        WHERE nominations = ?
        """, (winner, award))
     
    conn.commit()
    conn.close()


def main(date):
    start_id = get_start_id()
    artist_list = get_artist_list(date)

    create_grammy_table(cur, conn, artist_list, start_id)
    insert_grammy_data(cur, conn, listing_data, winners_data, artist_list)
    update_start_id(start_id + 25)

if __name__ == "__main__":
     main('2023-05-01')
