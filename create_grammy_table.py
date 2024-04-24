import sqlite3
import grammy
from billboard_read_api import get_artist_list

def create_grammy_table(cur, conn, start_id, listing_data, winners_data, artist_list):

    #cur.execute ("""DROP TABLE IF EXISTS Grammys """)

    limit = 25

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Grammy_artists (
            grammy_artist_id INTEGER PRIMARY KEY,
            grammy_artist_name TEXT UNIQUE)
        """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Grammy_awards (
            grammy_awards_id INTEGER PRIMARY KEY,
            grammy_award TEXT UNIQUE)
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS Grammys (
        artist_id INTEGER,
        award_id INTEGER,
        FOREIGN KEY (artist_id) REFERENCES Grammy_artists (grammy_artist_id),
        FOREIGN KEY (award_id) REFERENCES Grammy_awards (grammy_awards_id),
        PRIMARY KEY (artist_id, award_id)
    )""")


    
    artist_info = {}

    for nominees in listing_data.values():
        
        for nominee_with_song in nominees:
            nom_list = []
            if '—' in nominee_with_song:
                artist_name = nominee_with_song.split('—')[1].strip()
                nominee_name = nominee_with_song.split('—')[0].strip()
                nom_list.append(nominee_name)
                #print(artist_name)
            else:
                artist_name = nominee_with_song
                nom_list.append(artist_name)
            
                #print(artist_name)

            if artist_name not in artist_info.keys():
                artist_info[artist_name] = []
                if len(artist_info[artist_name] )== 0:
                    artist_info[artist_name].append({'noms': nom_list})


    for artist in artist_info.keys():
        win_list = []
        for winning_award, winner in winners_data.items():
            if artist in winner:
                win_list.append(winning_award)
        artist_info[artist].append({'winner' : win_list})       

    #print(artist_info)

    #print((list(artist_info.keys())))
    
    for i in range(start_id, start_id + limit):
        if i < len(artist_list):
            for grammy_award in winners_data:
                 cur.execute("INSERT OR IGNORE INTO Grammy_awards (grammy_award) VALUES (?)", (grammy_award,))
    
    for i in range(start_id, start_id + limit):
        if i < len(artist_list):
            for artist in list(artist_info.keys()):
                cur.execute("INSERT OR IGNORE INTO Grammy_artists (grammy_artist_name) VALUES (?)", (artist,))
    
    for i in range(start_id, start_id + limit):
        if i < len(artist_list):
            for artist, data in artist_info.items():
    # Default to an empty list if 'winner' is not found
                awards_won = []
                for item in data:
                    awards_won = item.get('winner', [])
                    if awards_won:  # This will be True if 'awards_won' is not empty
                        for award in awards_won:
                            cur.execute("""SELECT grammy_awards_id from Grammy_awards WHERE grammy_award = ? """, (award,))
                            award_ids = cur.fetchall()
                            print(award_ids)
                            for grammy_awards_id_tuple in award_ids:
                                # Unpack the tuple to get the actual ID
                                (grammy_awards_id,) = grammy_awards_id_tuple
                                cur.execute("""
                                        INSERT OR IGNORE INTO Grammys (artist_id, award_id)
                                        SELECT Grammy_artists.grammy_artist_id, Grammy_awards.grammy_awards_id
                                        FROM Grammy_artists, Grammy_awards 
                                        WHERE Grammy_artists.grammy_artist_name = ? AND Grammy_awards.grammy_award = ?
                                    """, (artist, grammy_awards_id))
    #print("done")
    conn.commit()


def update_start_id(start_id):
    with open('grammy_start_id.txt', 'w') as file:
        file.write(str(start_id))

def get_start_id():
    with open('grammy_start_id.txt', 'r') as file:
        return int(file.readline())


def main(date):
    conn = sqlite3.connect('artist.db')
    cur = conn.cursor()
    start_id = get_start_id()
    artist_list = get_artist_list(date)

    listing_data = grammy.retrieve_listings()
    winners_data = grammy.get_winners()


    create_grammy_table(cur, conn, start_id, listing_data, winners_data, artist_list)
    update_start_id(start_id + 25)

    conn.close()

if __name__ == "__main__":
     main('2023-05-01')
