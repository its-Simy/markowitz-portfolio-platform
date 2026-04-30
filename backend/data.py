import os
import time
from dotenv import load_dotenv
from typing import Union
from pathlib import Path
import requests
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
    
    #Downloads CSV from Alpha Vantage, saves it, then passes it through clean
    def fetch(self, symbol:str, save_dir:str = "Downloaded_Data") -> None:
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ symbol +'&apikey=' + self.api_key + "&datatype=csv"
        dataRequest = requests.get(url)

        # Alpha Vantage returns a JSON-ish error body (not CSV) when rate-limited or on bad symbol.
        # Valid CSV starts with the header "timestamp,open,high,low,close,volume".
        if not dataRequest.text.lstrip().startswith("timestamp"):
            raise RuntimeError(f"Bad response for {symbol}: {dataRequest.text[:200]}")

        os.makedirs(save_dir, exist_ok=True)
        filepath = os.path.join(save_dir, f"{symbol}_data.csv")
        with open(filepath, 'w') as f:
            f.write(dataRequest.text)

        self.clean(symbol, filepath)

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    data = DataFetcher(api_key)

    symbols = ["NVDA", "GOOG", "IBM"]
    for i, symbol in enumerate(symbols):
        if i > 0:
            time.sleep(1.2)  # Respect 1 req/sec rate limit
        data.fetch(symbol, save_dir="Tester_Data")

    pickle_path = os.path.join("Tester_Data", "dataset.pkl")
    data.df.to_pickle(pickle_path)
    print(f"Pickled merged DataFrame ({data.df.shape}) to {pickle_path}")