from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest



def retrieve_listings(): 

    relative_path = f"https://www.npr.org/2023/02/02/1153442645/2023-grammy-awards-nominees-winners"

    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, relative_path)

    with  open(full_path, "r", encoding="utf-8-sig") as file:

        soup = BeautifulSoup(file, 'html.parser')

        genre_dic = {}
        award_dic = {}
        nominee_dic = {}
        winner_dic = {}

        genres = soup.find_all('h3', class_='edTag')
        strong_tags = soup.find_all('strong', class_='edTag')

        print(strong_tags)

        # listing_pattern = r'\/(\d+)'
        # new_list = []
        # id_list = []
        # returned_list = []

        # listing_names = soup.find_all('div', class_='t1jojoys')
        # listing_ids = soup.find_all('a', class_='l1j9v1wn bn2bl2p dir dir-ltr')

        # for listing in listing_names:
        #     new_list.append(listing.text)

        # for id in listing_ids:
        #     id_list.append(id.get('href'))

        # for itm in id_list:
        #     matchs = re.findall(listing_pattern, itm)
        #     for match in matchs:
        #         if match not in id_list:
        #             listings_data.append(match)

        # for i in range(len(new_list)):
        #     returned_list.append((new_list[i],listings_data[i]))
        
        # #print(returned_list)
        # return returned_list


    """
    make_listing_database(html_file) -> list

    [('Loft in Mission District', '1944564'), ('Home in Mission District', '49043049'), ...]

    TODO Write a function that takes in a variable representing the path of the search_results.html file then calls the functions retrieve_listings() and listing_details() in order to create and return the complete listing information. 
    
    This function will use retrieve_listings() to create an initial list of Airbnb listings. Then use listing_details() to obtain additional information about the listing to create a complete listing, and return this information in the structure: 

        [
        (Listing Title 1,Listing ID 1,Policy Number 1, Host Name(s) 1, Place Type 1, Average Review Score 1, Nightly Rate 1),
        (Listing Title 2,Listing ID 2,Policy Number 2, Host Name(s) 2, Place Type 2, Average Review Score 2, Nightly Rate 2), 
        ... 
        ]

    NOTE: retrieve_listings() returns a list of tuples where the tuples are of length 2, listing_details() returns just a tuple of length 5, and THIS FUNCTION returns a list of tuples where the tuples are of length 7. 

    Example output: 
        [('Loft in Mission District', '1944564', '2022-004088STR', 'Brian', 'Entire Room', 4.98, 181), ('Home in Mission District', '49043049', 'Cherry', 'Pending', 'Entire Room', 4.93, 147), ...]    
    """
    pass



def main (): 
    retrieve_listings()
    


if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)