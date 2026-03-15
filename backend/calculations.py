import pandas as pd
class calculations:
    def __init__(self,df:pd.DataFrame):
        self.df = df
        self.weights = []

    def getWeights(self) -> None:
        passed = False
        isZero = False
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
                
                if x == 0:
                    isZero= True
                self.weights.append(x)
                        
            if sum(self.weights) > 1 or sum(self.weights) < 1 or isZero:
                self.weights = []
                if(isZero):
                    print("Invalid input(s), all vlaues must be greater than zero. Try Again")
                else:
                    print("Invalid, must input decimals (floats) that sum up to 1, with none being 0. Try Again")
                isZero = False
            else:
                passed = True
    

            
        
    #def expected_return_P(self):


if __name__ == "__main__":
    info = calculations(pd.read_pickle("Tester_Data\\dataset.pkl"))
    info.getWeights()
    print(info.weights)



