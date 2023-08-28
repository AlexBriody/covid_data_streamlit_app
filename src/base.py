import requests
import pandas as pd
import os
from pathlib import Path


class Base:
    """
    Class handles all connection to the API object and returns a DataFrame from it's initialization.
    
    Class will have these methods:
    return_url: return the api_url that we are currently working with
    get_data: scrape the data from the API and create a dataframe from it
    """
    def __init__(self):
        self.api_url = 'https://api.coinranking.com/v2'
        self.df = self.get_data()
    
    def return_url(self):
        return self.api_url
    
    def get_data(self):
        ''' Scraping data from the API and creating a DataFrame from it.'''
        headers = {
        'x-access-token': 'coinranking591cd311d57696390361bc73e7583af6d635b618272d8595'
        }
        response = requests.request("GET", "https://api.coinranking.com/v2/coins", params={"orderBy": "marketCap", "limit": 5000})
        
        # Alternate response coding:
        # response = requests.get(self.api_url + "/coins", params={"orderBy": "marketCap", "limit": 5000})
        
        print(response.text)  # TEST: Print the JSON data     
        
        self.df = pd.DataFrame.from_dict(response)
        return self.df
    
if __name__ == '__main__':
    c = Base()

    # Establish the data folder directory and create the path:
    folder_dir = os.path.join(Path(__file__).parents[0], 'data')
    csv_path = os.path.join(folder_dir, "crypto_data.csv")

    c.df.to_csv(csv_path , index=False)

  
    