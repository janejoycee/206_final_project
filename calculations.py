import sqlite3
import matplotlib.pyplot as plt


### PART 3 - Process the data (50 points) - after you have gathered all your data.
# You must select some data from all of the tables in your database and calculate
# something from that data (20 points). You could calculate the count of how many items
# occur on a particular day of the week or the average of the number of items per day.
# You must do at least one database join to select your data for your calculations or

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


def find_top_ten(conn, cursor):
    try:
        # Execute SQL query to get the top ten nominations
        cursor.execute("SELECT * FROM Grammy_billboard_artists ORDER BY nominations_num DESC LIMIT 10")
        top_ten_nominations = cursor.fetchall()
        conn.commit()
        return top_ten_nominations

    except sqlite3.Error as e:
        print("Error reading data from SQLite table:", e)



    

def join_tables(conn, cursor):
    try:
        # Execute SQL query to join the tables and retrieve desired columns
        cursor.execute("""
            SELECT a.name, f.follower_count, p.popularity_index
            FROM Spotify_followers AS f
            JOIN Spotify_popularity AS p ON f.spotify_artist_id = p.spotify_artist_id
            JOIN artist AS a ON f.spotify_artist_id = a.identification
            ORDER BY f.follower_count DESC
        """)
        joined_data = cursor.fetchall()
        conn.commit()
        return joined_data


    except sqlite3.Error as e:
        print("Error reading data from SQLite tables:", e)


def top_ten_followers(conn, cursor):
    try:
        # Execute SQL query to get the top ten follower artists
        cursor.execute("""
            SELECT a.name, REPLACE(CAST(f.follower_count AS TEXT), ',', '') as formatted_follower_count
            FROM Spotify_followers AS f
            JOIN artist AS a ON f.spotify_artist_id = a.identification
            ORDER BY f.follower_count DESC
            LIMIT 10
        """)
        top_ten_data = cursor.fetchall()
        conn.commit()
        return top_ten_data

    except sqlite3.Error as e:
        print("Error reading data from SQLite tables:", e)

def plot_bar_chart(data):
    artist_names = [row[0] for row in data]
    follower_counts = [int(row[1]) / 1_000_000 for row in data]  # Convert follower counts to millions

    plt.figure(figsize=(10, 6))
    plt.barh(artist_names, follower_counts, color='skyblue')
    plt.xlabel('Number of Followers (Millions)')
    plt.ylabel('Artist Name')
    plt.title('Top Ten Follower Artists')
    plt.gca().invert_yaxis()
    plt.show()


        

def main(date):
    db_path = "artist.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()


    with open('final_calculations.txt', 'w') as f:
        output = calculate_average_follower_count(conn, cur)
        formatted_avg_follower_count = "{:,.2f}".format(output)
        f.write(f"AVG NUM OF FOLLOWERS = {formatted_avg_follower_count}\n")


        pop_output = calculate_average_popularity_index(conn, cur)
        formatted_avg_pop_index = "{:,.2f}".format(pop_output)
        f.write(f"AVG POPULARITY INDEX = {formatted_avg_pop_index}\n")

        nom_output = calculate_average_grammy_nomination(conn, cur)
        formatted_avg_grammy_nom = "{:,.2f}".format(nom_output)
        f.write(f"AVG GRAMMY NOMINATION = {formatted_avg_grammy_nom}\n")


        top_ten_nominations = find_top_ten(conn, cur)
        if top_ten_nominations:
            f.write("\nTop Ten Nominations:\n")
            for index, nomination in enumerate(top_ten_nominations, 1):
                artist_name = nomination[0]  # Assuming the artist name is in the first column
                nominations_num = nomination[1]  # Assuming the nominations number is in the second column
                f.write(f"{index}. Artist: {artist_name}, Nominations: {nominations_num}\n")

            top_ten_avg = sum(nomination[1] for nomination in top_ten_nominations) / len(top_ten_nominations)
            f.write(f"AVG GRAMMY NOMINATION FOR TOP TEN ARTISTS: {top_ten_avg}\n")

        else:
            f.write("No data found.")


        joined_data = join_tables(conn, cur)
        if joined_data:
            # Determine maximum width for each column
            max_name_width = max(len(row[0]) for row in joined_data)
            max_follower_count_width = max(len(str(row[1])) for row in joined_data)
            max_popularity_index_width = max(len(str(row[2])) for row in joined_data)

            # Print header
            print(f"{'Artist Name':<{max_name_width}} | {'Follower Count':<{max_follower_count_width}} | {'Popularity Index':<{max_popularity_index_width}}")
            print("-" * (max_name_width + max_follower_count_width + max_popularity_index_width + 6))  # Total width of the header

            # Print data
            for row in joined_data:
                artist_name, follower_count, popularity_index = row
                # Format the follower count with commas and pad to match maximum width
                formatted_follower_count = "{:>{width},}".format(int(follower_count), width=max_follower_count_width)
                print(f"{artist_name:<{max_name_width}} | {formatted_follower_count} | {popularity_index:<{max_popularity_index_width}}")
        else:
            print("No data found.") 


    top_ten_data = top_ten_followers(conn, cur)
    if top_ten_data:
        plot_bar_chart(top_ten_data)
    else:
        print("No data found.")


        


    conn.close()

if __name__ == "__main__":
    main('2023-05-01')

