
import requests
import json
import unittest
import os


def get_rank_artist_data(date):
    '''
    creates API request for billboard API
    argument:  date inputted by user in YYYY-MM-DD string format

    '''
    top_100_artist_dict = {}
    params = {
        'date': date,
        'range': '1-100' 
        }

    headers = {
        "X-RapidAPI-Key": "b008c27844mshb83c2d80a68d5a5p108975jsn17b2b8e3d1a4",
	    "X-RapidAPI-Host": "billboard-api2.p.rapidapi.com"
        }

    base_url = "https://billboard-api2.p.rapidapi.com/artist-100"
        
    response = requests.get(base_url, headers=headers, params=params)
    if response.ok:
        weekly_top_artists = response.json()


        if 'content' in weekly_top_artists:
            rank_info = weekly_top_artists['content']
            
            for rank,artist_info in rank_info.items():
                artist_name = artist_info['artist']
                if artist_name not in top_100_artist_dict:
                    top_100_artist_dict[artist_name] = artist_info
            else:
                print("Billboard Top Artist Chart Not Found")

    return top_100_artist_dict


def get_artist_list(date):
    artist_dict = get_rank_artist_data(date)
    artist_list = list(artist_dict.keys())
    return artist_list



    
def main():
    '''
    Call functions here.
    '''
    billboard_artist_json = get_rank_artist_data('2023-05-01')
    print(billboard_artist_json)


if __name__ == "__main__":
    main()
