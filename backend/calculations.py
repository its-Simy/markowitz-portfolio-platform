import pandas as pd
from decimal import *
class calculations:
    def __init__(self,df:pd.DataFrame):
        self.df = df #time stamps are organized as smaller index = more recent
        self.weights = [] #list of weights for the tickers, in order to the dataframe
        self.assetReturns = []#list of calculated asset returns, in order to the dataframe
        self.portfolioReturn = 0 # total estimated portfolio return
        self.covarianceMatrix = []#2d list representing the covariance matrix.
    
    #ask user for the weights of each ticker
    #total inputs must equal 1 (asks user for input again if result is over or under along with if inputs are not floats)
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
        for label in self.df:
            if label == 'timestamp':
                continue
            count = 0
            total = 0
            #backtrack since 99 is the latest item in the list. then skip it to have a prev
            #consult prof about how to increase decimal accuracy? Floats won't cut it, but it should get most of the job done.
            for price in reversed(self.df.index):
                if count == 0:
                    prev = self.df.loc[price,label]
                    count += 1
                    continue
                #(current price - (current price location + 1)) / (current price location + 1)
                current = self.df.loc[price,label]
                day_price = (current - prev) / prev
                prev = self.df.loc[price,label]
                total += (day_price * 1/99)
            self.assetReturns.append(total)

    #calculate Expected Return of portfolio
    def expected_return_portfolio(self):
        self.getWeights()
        self.expected_return_asset()
        for point in range(len(self.weights)):
            self.portfolioReturn += (self.weights[point] * self.assetReturns[point])

    
    def covariance_Calculations(self):
        #covariance matrix is split into two parts
        #the main diagonal ([1][1],[2][2],...[n][n]) should consist of variants per asset
        #uses the equation (Summation of (daily return * average return)^2 / number of observations
        #For non diagonals which are covariants, we use the following equation
        #(summation of (daily return of asset 1 - mean return of asset 1)* (daily return of asset 2 - mean return of asset 2)) / number of observations aka number of items - 1
        # asset 1 in this case would be whatever the main diagonal asset we are currently on for that row, asset 2 would be whatever col we are on.
        
        

if __name__ == "__main__":
    info = calculations(pd.read_pickle("Tester_Data\\dataset.pkl"))    
    info.expected_return_portfolio()
    print("Asset Weights: ",info.weights)
    print("Asset Returns: ",info.assetReturns)
    print("Return: ",info.portfolioReturn)
    



