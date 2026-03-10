import os
from dotenv import load_dotenv
import requests
import io
import pandas as pd

class DataFetcher:
    def __init__(self,api_key:str,df:pd.DataFrame):
        self.api_key = api_key
        self.df = df
    
    #only adjusts Dataframe, so doesn't have to return anything
    def fetch(self, symbol:str) -> None:
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ symbol +'&apikey=' + self.api_key + "&datatype=csv"#calls the url, fetches data using requests
        dataRequest = requests.get(url)# loads csv data.
        #Add data to the datframe
        new_data = pd.read_csv(io.StringIO(dataRequest.text))
        new_data['symbol'] = symbol
        self.df = pd.concat([self.df,new_data],ignore_index=True)#adjusts current dataframe with the new info
        

if __name__ == "__main__":
    #loads api key
    load_dotenv()
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    df = pd.DataFrame()
    DataFetcher(api_key,df)
