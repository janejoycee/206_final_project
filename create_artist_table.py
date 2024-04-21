import sqlite3
import os
import json
from billboard_read_api import get_artist_list


def create_artist_table(cur, conn, artist_list, start_id):
    limit = 25
    cur.execute("CREATE TABLE IF NOT EXISTS Artist (identification INTEGER PRIMARY KEY, name TEXT)")

    for i in range(start_id, start_id + limit):
        if i < len(artist_list):
            cur.execute("INSERT INTO Artist (identification, name) VALUES (?, ?)",
                        (i, artist_list[i]))
    conn.commit()

def update_start_id(start_id):
    with open('start_id.txt', 'w') as file:
        file.write(str(start_id))

def get_start_id():
    with open('start_id.txt', 'r') as file:
        return int(file.readline())

def main(date):
    conn = sqlite3.connect('artist.db')
    cur = conn.cursor()
    artist_list = get_artist_list(date)
    start_id = get_start_id()

    create_artist_table(cur, conn, artist_list, start_id)
    update_start_id(start_id + 25)

    conn.close()

if __name__ == "__main__":
    main('2023-05-01')