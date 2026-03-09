import os
from dotenv import load_dotenv

class data():
    load_dotenv()
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    #Parsing
    


if __name__ == "__main__":
    data()
