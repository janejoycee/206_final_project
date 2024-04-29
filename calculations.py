import sqlite3
import matplotlib.pyplot as plt
import numpy as np


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


def top_ten_popularity(conn, cursor):
    try:
        # Execute SQL query to get the top ten artists by popularity index
        cursor.execute("""
            SELECT a.name, p.popularity_index
            FROM Spotify_popularity AS p
            JOIN artist AS a ON p.spotify_artist_id = a.identification
            ORDER BY p.popularity_index DESC
            LIMIT 10
        """)
        top_ten_data = cursor.fetchall()
        conn.commit()
        return top_ten_data

    except sqlite3.Error as e:
        print("Error reading data from SQLite tables:", e)


def plot_bar_chart_followers(data):
    artist_names = [row[0] for row in data]
    follower_counts = [int(row[1]) / 1_000_000 for row in data]  # Convert follower counts to millions

    plt.figure(figsize=(10, 6))
    plt.barh(artist_names, follower_counts, color='skyblue')
    plt.xlabel('Number of Followers (Millions)')
    plt.ylabel('Artist Name')
    plt.title('Top Ten Follower Artists')
    plt.gca().invert_yaxis()
    plt.show()


def plot_bar_chart_popularity(data):
    artist_names = [row[0] for row in data]
    popularity_index = [row[1] for row in data]

    plt.figure(figsize=(10, 6))
    bars = plt.barh(artist_names, popularity_index, color='pink')
    plt.xlabel('Popularity Index')
    plt.ylabel('Artist Name')
    plt.title('Top Ten Artists by Popularity Index')
    plt.gca().invert_yaxis()
    plt.xlim(80, 100)  # Set x-axis limits from 80 to 100
    
    # Add popularity index values to the right of the bars
    for bar, index in zip(bars, popularity_index):
        plt.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2, f'{index:.2f}', va='center')

    plt.show()




def plot_dual_bar_graph(follower_data, popularity_data):
    artist_names = [row[0] for row in follower_data]
    follower_counts = [int(row[1]) / 1_000_000 for row in follower_data]  # Convert follower counts to millions
    popularity_index = [row[1] for row in popularity_data]

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Define width of each bar
    bar_width = 0.35

    # Calculate x-axis positions for the bars
    x = np.arange(len(artist_names))

    # Plot follower count as the first bar graph on the left y-axis
    color1 = 'skyblue'
    ax1.bar(x - bar_width/2, follower_counts, color=color1, width=bar_width, label='Follower Count (Millions)')
    ax1.set_xlabel('Artist Name')
    ax1.set_ylabel('Follower Count (Millions)')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_xticks(x)
    ax1.set_xticklabels(artist_names, rotation=45, ha='right')
    ax1.set_ylim(0, max(follower_counts) * 1.1)  # Adjust y-axis limits for better visibility

    # Create a secondary y-axis for popularity index
    ax2 = ax1.twinx()

    # Plot popularity index as the second bar graph on the right y-axis
    color2 = 'lightgreen'
    ax2.bar(x + bar_width/2, popularity_index, color=color2, width=bar_width, label='Popularity Index')
    ax2.set_ylabel('Popularity Index')
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.set_ylim(80, 100)  # Set y-axis limits for popularity index from 0 to 100


    for i, index in enumerate(popularity_index):
        ax2.text(x[i] + bar_width/2, index + 1, str(index), ha='center', va='bottom')

    plt.title('Top Ten Artists: Follower Count and Popularity Index')

    # Show legend for both bar graphs
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.tight_layout()


        

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
        plot_bar_chart_followers(top_ten_data)
    else:
        print("No data found.")


    top_ten_data = top_ten_popularity(conn, cur)
    if top_ten_data:
        plot_bar_chart_popularity(top_ten_data)
    else:
        print("No data found.")
        

    top_ten_followers_data = top_ten_followers(conn, cur)
    top_ten_popularity_data = top_ten_popularity(conn, cur)
    plot_dual_bar_graph(top_ten_followers_data, top_ten_popularity_data)

    plt.show()


        


    conn.close()

if __name__ == "__main__":
    main('2023-05-01')

