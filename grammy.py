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

    print(award_dic)
    print(len(award_dic))
    
    return award_dic



def get_winners ():
    #this function gets the winners for every category, and adds it to a list

        
    
    pass



def main (): 
    retrieve_listings()
    


if __name__ == '__main__':
    main()
    #unittest.main(verbosity=2)