from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest



def retrieve_listings(): 

    relative_path = "/2023/02/grammys-2023-full-list-of-winners.html"

    base_url = "https://www.vulture.com/"
    full_url = base_url + relative_path

    
    response = requests.get(full_url)
    if response.status_code != 200:  # Checks if the request was successful
        print('Failed to retrieve content.')
        return None
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    award_dic = {}
    nominee_list = []

    categories =  soup.find_all('p', class_='clay-paragraph')

    for category in categories:  
        award_name_element = category.find('strong')
        if award_name_element: 
            award_name = award_name_element.text.strip()
        else:
            continue
        
        nominee_strings = category.get_text(separator="\n").split('\n')
        
        nominee_strings = [nominee for nominee in nominee_strings if nominee and nominee != award_name]
        
        if nominee_strings:
            award_dic[award_name] = nominee_strings
    print(award_dic)
    
    return award_dic



















#     genres = soup.find_all('h3', class_='edTag')
#     for genre in genres:
#         genre = genre.text
#         #print(genre)
#         genre_list.append(genre)
#         #should be 27
    
#    # print(genre_list)
#     #print(len(genre_list))

#     strong_tags_inside_p = soup.find_all('p')  # Find all <p> tags
#     for p_tag in strong_tags_inside_p:
#         strong_tags = p_tag.find_all('strong')  # Find all <strong> tags inside each <p> tag
#         for strong_tag in strong_tags:
#             strong_text = strong_tag.get_text()
#             match = re.match(title_regex, strong_text)
#             if match:
#                 title = match.group(1)
#                 #print(title)
#                 if title not in award_dic:
#                     award_dic[title] = []
    
#     print(award_dic)

#     edTag_ul = soup.find_all('ul', class_='edTag')

#     for edTag in edTag_ul: #for every award in a list of awards
#         #print(edTag)

#         song_and_artist_noms = edTag.find_all('li') #get every awards nominations

#         winner_text = ""

#         for item in song_and_artist_noms:
#             #print(item)
#             if "WINNER:" in item:
#                 continue  # Skip to the next item if "WINNER:" is found
#             text = item.text
#             print(text)
        
#             if "WINNER:" in text:
#                 winner_start_index = text.find("WINNER:") + len("WINNER:")
#                 winner_text = text[winner_start_index:].strip()
#                 winner_but_no_label = text.replace("WINNER: ", "")
#                 #print(winner_but_no_label)

#         print("Winner text:", winner_text)
        
        # to seperate the artist by the song, do whatever is in quotes
        # is there something that seperates it by italics





            

        
    
    pass



def main (): 
    retrieve_listings()
    


if __name__ == '__main__':
    main()
    #unittest.main(verbosity=2)