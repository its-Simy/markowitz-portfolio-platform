import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
class Calculations:

    def __init__(self,df):
        self.df = df.iloc[::-1] # just makes the df items reverse, as we want to focus on latest to more recent
        self.dailyReturns = self.df.iloc[:,1:].pct_change().dropna()# would calculate the returns, and drop the last item since it wouldn't have any, and skips first col to avoid any attempt to do math on strings
        self.meanReturns = self.dailyReturns.mean() #takes mean of each column and returns a series with the returns
        self.covMatrix = self.dailyReturns.cov()#uses the built in covariance matrix method
        self.numObservations = len(self.dailyReturns)#how many daily returns days we see
        self.riskFreeRate = .0369 #needs to be made dynamic!!


    def minimum_variance_portfolio(self):
        #if this isn't possible we must do the Moore-Penrose pseudoinverse, this is because that would imply the matrix is singular
        try:
            inverseCovariance = np.linalg.inv(np.array(self.covarianceMatrix))
        except np.linalg.LinAlgError:
            inverseCovariance = np.linalg.pinv(np.array(self.covarianceMatrix))
        
        ones = np.ones(len(self.weights))
        mvp = (inverseCovariance.dot(ones)) / ((ones[:np.newaxis].dot(inverseCovariance)).dot(ones))
        self.mvp = mvp

    #-------performance calculations-----------
    def portfolio_annualized_performance(self,meanReturns,weights,covMatrix):
        returns = np.sum(meanReturns * weights) * 252 #multiplies it by the estimated 252 trading days
        std = np.sqrt(np.dot(weights.T,np.dot(covMatrix,weights)))* np.sqrt(252)
        #Square root of (weights transpose * (covariance matrix * weights)) * square root of 252
        return std,returns
    
    #STILL NEEDS TO BE FIXED
    def sharpe_ratio(self):
        #.0369 is the us treasury bond 3 month maturity rate, in the future remove hard coding of this, only hard coded for testing purposes, also we are dividing since we are using daily returns we must have daily rate
        return (self.portfolioReturn - (.0369 / 252)) / self.portfolio_standard_deviation()

    #------PLOTS--------
    def plotAssetReturns(self):
        plt.figure(figsize=(14,7))
        for label in self.df.iloc[:,1:]:
            plt.plot(self.dailyReturns.loc[:,label], linewidth=2.0, label=label)
        plt.title("Asset Returns Over Time")
        plt.legend(loc='upper left', fontsize=12)
        plt.ylabel("Daily Return")
        st.pyplot(plt)
    
    def plotAssets(self):
        plt.figure(figsize=(14,7))
        plotData = self.df[::-1]
        for c in plotData.columns[1:].values:
            plt.plot(self.df.index, plotData[c], lw=3, alpha=0.8,label=c)
        plt.title("Asset Pricing Over Time")
        plt.legend(loc='upper left', fontsize=12)
        plt.ylabel('price in $')
        st.pyplot(plt)
    
    def plotFrontier(self,results,weights):
        maxSharpeIndex = np.argmax(results[2])
        stdBestPortfolio = results[0,maxSharpeIndex]
        returnPortfolio = results[1,maxSharpeIndex]
        max_sharpe_allocation = pd.DataFrame(weights[maxSharpeIndex],index=self.df.columns[1:],columns=['allocation'])
        max_sharpe_allocation.allocation = [round(i*100,2)for i in max_sharpe_allocation.allocation]
        max_sharpe_allocation = max_sharpe_allocation.T
        min_vol_idx = np.argmin(results[0])
        sdp_min, rp_min = results[0,min_vol_idx], results[1,min_vol_idx]
        min_vol_allocation = pd.DataFrame(weights[min_vol_idx],index=self.df.columns[1:],columns=['allocation'])
        min_vol_allocation.allocation = [round(i*100,2)for i in min_vol_allocation.allocation]
        min_vol_allocation = min_vol_allocation.T
        
        print("-"*80)
        print("Maximum Sharpe Ratio Portfolio Allocation\n")
        print("Annualised Return:", round(returnPortfolio,2))
        print("Annualised Volatility:", round(stdBestPortfolio,2))
        print("\n")
        print(max_sharpe_allocation)
        print("-"*80)
        print("Minimum Volatility Portfolio Allocation\n")
        print("Annualised Return:", round(rp_min,2))
        print("Annualised Volatility:", round(sdp_min,2))
        print("\n")
        print(min_vol_allocation)

        plt.figure(figsize=(10, 7))
        plt.scatter(results[0,:],results[1,:],c=results[2,:],cmap='RdYlGn', marker='o', s=10, alpha=0.3)
        plt.colorbar()
        plt.scatter(stdBestPortfolio,returnPortfolio,marker='.',color='r',s=500, label='Maximum Sharpe ratio')
        plt.scatter(sdp_min,rp_min,marker='.',color='b',s=500, label='Minimum volatility')
        plt.title('Simulated Portfolio Optimization based on Efficient Frontier')
        plt.xlabel('annualised volatility')
        plt.ylabel('annualised returns')
        plt.legend(labelspacing=0.8)
        st.pyplot(plt)
        

    #---------general simulation--------
    #portfolio_annualized_performance(self,meanReturns,weights,covMatrix):
    def populateSimulation(self,numPortfolios: int,meanReturns,covarianceMatrix):
        results = np.zeros((3,numPortfolios))
        weights_record = []
        for i in range(numPortfolios):
            weights = np.random.random(len(self.df.columns)-1) #creates random weights for all the assets
            weights /= np.sum(weights)
            weights_record.append(weights)
            portfolioStdDev, portfolioReturn = self.portfolio_annualized_performance(meanReturns,weights,covarianceMatrix)
            results[0,i] = portfolioStdDev
            results[1,i] = portfolioReturn
            results[2,i] = (portfolioReturn - self.riskFreeRate) / portfolioStdDev
        return results,weights_record
    
    #-------Begins Simulation-------------
    def simulationStart(self, numPortfolios: int):
        self.plotAssets()
        self.plotAssetReturns()
        results,weights = self.populateSimulation(numPortfolios,self.meanReturns,self.covMatrix)
        self.plotFrontier(results,weights)

#-----main-------
if __name__ == "__main__":
    info = Calculations(pd.read_pickle("Tester_Data\\dataset.pkl"))   
    print(info.df)
    info.simulationStart(25000)
    
