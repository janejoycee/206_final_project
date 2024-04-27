import sqlite3

def calculate_average_follower_count(conn, cursor):
    try:
        # Execute SQL query to get the average follower count
        cursor.execute("SELECT AVG(follower_count) FROM Spotify_followers")
        average_follower_count = cursor.fetchone()[0]
        conn.commit()
        return average_follower_count

    except sqlite3.Error as e:
        print("Error reading data from SQLite table:", e)


def calculate_average_popularity_index(conn, cursor):
    try:
        cursor.execute("SELECT AVG(popularity_index) FROM Spotify_popularity")
        average_pop_index = cursor.fetchone()[0]
        conn.commit()
        return average_pop_index

    except sqlite3.Error as e:
        print("Error reading data from SQLite table:", e)


def calculate_average_grammy_nomination(conn, cursor):
    try:
        cursor.execute("SELECT AVG(nominations_num) FROM Grammy_billboard_artists")
        average_grammy_nom = cursor.fetchone()[0]
        conn.commit()
        return average_grammy_nom

    except sqlite3.Error as e:
        print("Error reading data from SQLite table:", e)






        

def main(date):
    db_path = "artist.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    output = calculate_average_follower_count(conn, cur)
    formatted_avg_follower_count = "{:,.2f}".format(output)
    print(f"AVG NUM OF FOLLOWERS = {formatted_avg_follower_count}")


    pop_output = calculate_average_popularity_index(conn, cur)
    formatted_avg_pop_index = "{:,.2f}".format(pop_output)
    print(f"AVG POPULARITY INDEX = {formatted_avg_pop_index}")

    nom_output = calculate_average_grammy_nomination(conn, cur)
    formatted_avg_grammy_nom = "{:,.2f}".format(nom_output)
    print(f"AVG GRAMMY NOMINATION = {formatted_avg_grammy_nom}")


    conn.close()

if __name__ == "__main__":
    main('2023-05-01')

