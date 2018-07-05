
# The strategy said that investor sells after a 2% down-day and buys back 20 trading days later.
# Assume the transaction fee is 0.0001 and investor had 1000 shares of S&P500 in 1960.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys, os
from os import path
class Panic(object):
    def __init__(self, share,data_value, tran):
        self.share = share
        self.data_value=data_value
        self.tran = tran

    def BackTest(self):
        # tran is transaction fee
        sell_day = -1;
        k = 1;
        data_value =self.data_value
        share=self.share
        tran=self.tran
        n = len(data_value)
        
        money = [0]*n
        money = [0]*n
        money[0] = share*data_value.iloc[0][1];
        for a in range (1,n-1):
            
            ## keep the share
            if(k ==1):
                money[a] = share*data_value.iloc[a][1]
            if a == sell_day:
            ## buy the stock back
                share = money[sell_day-1]*(1-tran)/(data_value.iloc[sell_day][1])
                k=1
            ## determine sell the stock or not
            elif ((data_value.iloc[a][1]-data_value.iloc[a-1][1])/data_value.iloc[a][1] < -0.02)&(a > sell_day):
            ## sell the share and keep money 20 days
                k=0
                if(a<n-21):
                    sell_day = a+20
                    money[a:a+20] = [data_value.iloc[a][1]*share*(1-tran)]*20
                else:
            ## determine whether in [n-20,20]
                    money[a:len(a)-1] = [data_value.iloc[a][1]*share*(1-tran)]*(len(a)-1-a)
                    break;
        ## def a function to plot time series
        def DEF(x):
            return pd.to_datetime(x, format="%Y/%m/%d")
        
        
        
        data_value['Date']=DEF(data_value['Date'])
        tsdata_value=data_value.set_index('Date')
        tsMoney=pd.Series(money,index=tsdata_value.index)
        tsMoney[tsMoney==0]=pd.np.nan
        fig= plt.figure()
        ax1=fig.add_subplot(1,1,1);ax2 = ax1.twinx()
        ax1.plot(tsMoney.dropna(),label='Money',color='r')
        ax2.plot(tsdata_value.dropna(),label='SP500',color='b')
        plt.figure(figsize=(12,8),facecolor='1.0') 
        plt.show()
if __name__=="__main__":
    data = pd.read_csv(path.expanduser('~/Documents/Data/sp500.csv'))
    bt=Panic(1000,data,0.0001)
    bt.BackTest()    
    


