import pandas as pd
class calculations:
    def __init__(self,df:pd.DataFrame):
        self.df = df #time stamps are organized as smaller index = more recent
        self.weights = []
        self.assetReturns = []
        self.portfolioReturn = 0
        

    def getWeights(self) -> None:
        passed = False
        inValid = False
        while not passed:
            for name in self.df.columns:
                if name == "timestamp":
                    continue
                x = -1
                while True:
                    try:
                        x = float(input(f"What is the current weight for {name}: "))
                        break
                    except ValueError:
                        print("Only integers are valid inputs")
                
                if x <= 0:
                    inValid= True
                self.weights.append(x)
                        
            if sum(self.weights) > 1 or sum(self.weights) < 1 or inValid:
                self.weights = []
                if(inValid):
                    print("Invalid input(s), all vlaues must be greater than zero. Try Again")
                else:
                    print("Invalid, must input decimals (floats) that sum up to 1, with none being 0. Try Again")
                isZero = False
            else:
                passed = True
    #Calculated expected return of an asset within the portfolio
    def expected_return_asset(self):
        #we must parse through the dataframe, at point end - 1, until the most recent to use and calculate daily return
        #backtrack from column length - 2 until 0
        #(current price - (price location + 1)) / (price location + 1)
        for label in self.df:
            if label == 'timestamp':
                continue
            count = 0
            total = 0
            for price in reversed(self.df.index):
                if count == 0:
                    prev = price
                    count += 1
                    continue
                day_price = (price - prev) / prev
                prev = price
                total += (day_price * 1/99)
            self.assetReturns.append(total)

    #calculate Expected Return of portfolio
    def expected_return_Portfolio(self):
        for point in range(len(self.weights)):
            self.portfolioReturn += (self.weights[point] * self.assetReturns[point])

if __name__ == "__main__":
    info = calculations(pd.read_pickle("Tester_Data\\dataset.pkl"))
    #info.getWeights()
    #print(info.weights)
    info.expected_return_asset()



