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


    genre_list = []
    award_dic = {}
    nominee_list = []
    winner_dic = {}
    title_regex = r'\d+\.\s*(.+)'

    genres = soup.find_all('h3', class_='edTag')
    for genre in genres:
        genre = genre.text
        #print(genre)
        genre_list.append(genre)
        #should be 27
    
    print(genre_list)
    #print(len(genre_dic))

    strong_tags_inside_p = soup.find_all('p')  # Find all <p> tags
    for p_tag in strong_tags_inside_p:
        strong_tags = p_tag.find_all('strong')  # Find all <strong> tags inside each <p> tag
        for strong_tag in strong_tags:
            strong_text = strong_tag.get_text()
            match = re.match(title_regex, strong_text)
            if match:
                title = match.group(1)
                #print(title)
                if title not in award_dic:
                    award_dic[title] = {}
    
    #print(award_dic)

    edTag_ul = soup.find('ul', class_='edTag')

    song_and_artist_noms = edTag_ul.find_all('li')

    winner_text = ""

    for item in song_and_artist_noms:
        #print(item)
        if "WINNER:" in item:
            continue  # Skip to the next item if "WINNER:" is found
        text = item.text
        print(text)

        if "WINNER:" in text:
            winner_start_index = text.find("WINNER:") + len("WINNER:")
            winner_text = text[winner_start_index:].strip()
            winner_but_no_label = text.replace("WINNER: ", "")
            print(winner_but_no_label)

    print("Winner text:", winner_text)



            

        
    
    pass



def main (): 
    retrieve_listings()
    


if __name__ == '__main__':
    main()
    #unittest.main(verbosity=2)