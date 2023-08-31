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
        self.api_url = 'https://api.collectapi.com/corona/countriesData'
        self.headers = {
            'content-type': "application/json",
            'authorization': "apikey 6E0Xk78UZVTEIyfpfB29rO:33l7pSNe73xSkZm0tr2Qdm"
        }
        self.df = self.get_data()
    
    def return_url(self):
        return self.api_url
    
    def get_data(self):
        ''' Scraping data from the API and creating a DataFrame from it.'''
        response = requests.get(self.api_url, headers=self.headers)
        
        if response.status_code == 200:
            # print(response.text) 
            print("Connection successful!!!")
            json_data = response.json()

            # Extract the 'result' field from the JSON data
            list_of_dicts = json_data.get('result', [])
            self.df = pd.DataFrame(list_of_dicts)
        else:
            print("Connection not successful. Status code:", response.status_code)
                    
        return self.df
    
if __name__ == '__main__':
    c = Base()

    # File path problem: filepath to .csv not recognized
    # Establish the data folder directory and create the path to .csv:
    folder_dir = os.path.join(Path(__file__).parents[0], 'data')
    csv_path = os.path.join(folder_dir, "covid_data.csv")

    # Setting index to 'country' column as data has no index column
    c.df.set_index('country', inplace=True)
    c.df.to_csv(csv_path, index=True)

  
    