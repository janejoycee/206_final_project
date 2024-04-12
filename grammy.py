from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest



def retrieve_listings(): 

    relative_path = "/2023/02/02/1153442645/2023-grammy-awards-nominees-winners"

    base_url = "https://www.npr.org"
    full_url = base_url + relative_path

    # Fetch HTML content from the URL
    response = requests.get(full_url)
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')


    genre_dic = {}
    award_dic = {}
    nominee_list = []
    winner_dic = {}
    title_regex = r'\d+\.\s*(.+)'
    winner_regex = r'^"WINNER:"\s*(.+)'

    genres = soup.find_all('h3', class_='edTag')
    #print(genres)

    strong_tags_inside_p = soup.find_all('p')  # Find all <p> tags
    for p_tag in strong_tags_inside_p:
        strong_tags = p_tag.find_all('strong')  # Find all <strong> tags inside each <p> tag
        for strong_tag in strong_tags:
            strong_text = strong_tag.get_text()
            match = re.match(title_regex, strong_text)
            if match:
                title = match.group(1)
                #print(title)

    edTag_ul = soup.find('ul', class_='edTag')

    song_and_artist_noms = edTag_ul.find_all('li')

    winner_text = ""

    for item in song_and_artist_noms:
        text = item.text
        #print(text)
        
        
        if "WINNER:" in text:
            winner_start_index = text.find("WINNER:") + len("WINNER:")
            winner_text = text[winner_start_index:].strip()

    print("Winner text:", winner_text)

            

        
    
    pass



def main (): 
    retrieve_listings()
    


if __name__ == '__main__':
    main()
    #unittest.main(verbosity=2)