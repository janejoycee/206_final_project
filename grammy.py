from bs4 import BeautifulSoup
import requests



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

    categories =  soup.find_all('p', class_='clay-paragraph')
    
    for category in categories:
        award_name_element = category.find('strong')
        if award_name_element:
            award_name = award_name_element.text.strip()
            award_name_element.extract()
        else:
            continue
        
        nominee_lines = list(category.stripped_strings)
        #print((nominee_lines))

        combined_list = []
        # pattern = re.compile(r'“(.*?)”\s*—\s*(.*)')
        prev_string = ""
        for line in nominee_lines:
            if '—' in line:
                if prev_string:
                    line = prev_string + ' ' + line
                combined_list.append(line)
                prev_string = ""  
            else:
                prev_string = line  

            if prev_string:  
                combined_list.append(prev_string)

        #print(combined_list)
        award_dic[award_name] = combined_list

    #print(award_dic)
   # print(len(award_dic))
    
    return award_dic



def get_winners ():

    relative_path = "/2023/02/grammys-2023-full-list-of-winners.html"

    base_url = "https://www.vulture.com/"
    full_url = base_url + relative_path

    
    response = requests.get(full_url)
    if response.status_code != 200:  # Checks if the request was successful
        print('Failed to retrieve content.')
        return None
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    winner_dict = {}

    categories =  soup.find_all('p', class_='clay-paragraph')

    for award_list in categories:
        strong_elements = award_list.find_all('strong')
        #print(strong_elements)

        if len(strong_elements) >= 2:
            award_name = strong_elements[0].get_text(strip=True)
            winner = strong_elements[1].get_text(strip=True)
            #print(f"The winner for {award_name} is {winner}")
            winner_dict[award_name] = winner
        #else:
            #print("Not enough <strong> elements within this category to determine the award and the winner.")

    #print(winner_dict.keys())

    #print(len(winner_dict))
    return winner_dict

    
    pass

def get_info_about_artist (artist):
    nom_dict = retrieve_listings()
    winner_dict = get_winners()
    artist_nom_info = {}
    artist_winning_info = {}

    for award_name, list_noms in nom_dict.items():
        for nom in list_noms:
            if artist in nom:
                if artist not in artist_nom_info:
                    artist_nom_info[artist] = []
                artist_nom_info[artist].append(award_name)

    for award_name, winner_list in winner_dict.items():
        if artist in winner_list:
            artist_winning_info[artist] = award_name


    if artist in artist_nom_info:
        print(f"The artist {artist} was nominated for {len(artist_nom_info[artist])} award(s): {artist_nom_info[artist]}.")
    else:
        print(f"The artist {artist} was not nominated for any awards.")

    if artist in artist_winning_info:
        print(f"They won the {artist_winning_info[artist]} award.")
    else:
        print(f"They did not win any awards.")
    
    pass
        


def main (): 
    retrieve_listings()
    get_winners()
    artist = "Some Artist"
    get_info_about_artist(artist)

    


if __name__ == '__main__':
    main()
    #unittest.main(verbosity=2)