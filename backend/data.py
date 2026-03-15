import os
from dotenv import load_dotenv
import requests
import io
import pandas as pd


class DataFetcher:
    def __init__(self,api_key:str):
        self.api_key = api_key
        self.df = pd.DataFrame()
        self.count = 0

    #This should clean add all the datasets to the dataframe and cleans up the structure
    #We only want the closing prices along with a singular time stamp
    def clean(self,symbol,filepath: Union[str,Path]) -> None:
        
        if self.count == 0:
            self.df = pd.read_csv(filepath)
            time = self.df.loc[:,'timestamp']
            closing_data = self.df.loc[:,'close']
            self.df = pd.concat([time,closing_data],axis=1)
        else:
            temp_data = pd.read_csv(filepath)
            closing_data = temp_data.loc[:,'close']
            self.df = pd.concat([self.df,closing_data],axis=1)

        self.df.rename(columns={'close':symbol},inplace=True)
        self.count += 1 
    
    #only adjusts Dataframe, so doesn't have to return anything
    def fetch(self, symbol:str) -> None:

        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ symbol +'&apikey=' + self.api_key + "&datatype=csv"#calls the url, fetches data using requests
        dataRequest = requests.get(url)# loads csv data.

        #Add data to the datframe
        new_data = pd.read_csv(io.StringIO(dataRequest.text))
        self.df = pd.concat([self.df,new_data],ignore_index=True)#adjusts current dataframe with the new info
        #Downloads the csv
        self.df.to_csv("Google_data",index=False)

    
        

if __name__ == "__main__":
    #loads api key
    
    load_dotenv()
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    data = DataFetcher(api_key)
    #for now we used data.fetch to downlaod the csv daily data, this allows us to not worry about rate limits
    #data.fetch("GOOG")
    data.clean("EFA","Tester_Data\\Barclays_data")
    data.clean("GOOG","Tester_Data\\Google_data")
    data.clean("IBM","Tester_Data\\Ibm_data")
    data.df.to_pickle("Tester_Data\\dataset.pkl")