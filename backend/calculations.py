import pandas as pd
class calculations:
    def __init__(self,df:pd.DataFrame):
        self.df = df


if __name__ == "__main__":
    start = calculations(pd.read_pickle("Tester_Data\\dataset.pkl"))
    print(start.df)


