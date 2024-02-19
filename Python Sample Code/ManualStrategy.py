

import datetime as dt
from indicators import *
import pandas as pd
from util import get_data
import os

class ManualStrategy(object):

    def author(self):
        return 'yhe600'  # replace tb34 with your Georgia Tech username.

    def Results(self, df_Benchmark,df_strategy,title,path,sv):
        ## normalized
        long_points = df_strategy[df_strategy['Transcation'] > 0].index  # Example data
        short_points = df_strategy[df_strategy['Transcation'] < 0].index  # Example data

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot(df_Benchmark.index,  df_Benchmark['Portfolio'] / sv, label= 'Benchmark', linestyle="-", color='purple')
        ax.plot(df_strategy.index, df_strategy['Portfolio'] / sv, label= 'Manual Strategy', linestyle="-", color='red')
        for long_entry in long_points[:-1]:
            ax.axvline(x=long_entry, color='blue', linestyle='--')

        for short_entry in short_points[:-1]:
            ax.axvline(x=short_entry, color='black', linestyle='--')

        ax.axvline(x=long_points[-1], color='blue', linestyle='--', label='Long Entry')
        ax.axvline(x=short_points[-1], color='black', linestyle='--', label='Short Entry')

        ax.set_xlabel("Date")
        ax.set_ylabel("Normalized Value")
        ax.legend()
        ax.set_title(title)
        ax.set_xlim(df_strategy.index[0], df_strategy.index[-1])
        # Use DateFormatter to format the x-axis
        date_format = mdates.DateFormatter('%Y-%m')
        ax.xaxis.set_major_formatter(date_format)
        plt.xticks(rotation=45)
        # Add grid lines
        ax.grid(True)
        plt.savefig(os.path.join(os.path.dirname(__file__), path.format()))
        plt.close()

    def testPolicy(self,symbol,sd,ed,sv):
        """
        I will use three indicators loaded from indicators.py
        1. Boollinger_Bands
        2. Stochastic_KD
        3. RSI
        If any selling/buy indicate from the indicators, check the position and do action.
        Equal weighted for these indicators
        """
        # here we build a fake set of trades
        # your code should return the same sort of data
        Commission = 9.95
        impact = 0.005
        dates = pd.date_range(sd, ed)
        prices_all = get_data([symbol],dates).astype(float)  # automatically adds SPY
        trades = prices_all[[symbol, ]]  # only portfolio symbols
        ## fill na
        trades = trades.fillna(method='ffill')
        trades = trades.fillna(method='bfill')

        BBands = Boollinger_Bands(symbol,sd,ed,14,figure= False)
        SKD = Stochastic_KD(symbol, sd,ed, 14, 3, figure= False)
        RSI_Results = RSI(symbol, sd,ed, 14, figure=False)
        # ## simulate portfolio value

        SKD['Signal'] = 0
        SKD.loc[(SKD['%D'] > 85) & (SKD['%K'] > 85), 'Signal'] = -1
        SKD.loc[(SKD['%D'] < 15) & (SKD['%K'] < 15), 'Signal'] = 1

        RSI_Results['Signal'] = 0
        RSI_Results.loc[RSI_Results['RSI'] > 75, 'Signal'] = -1
        RSI_Results.loc[RSI_Results['RSI'] < 25, 'Signal'] = 1

        ## initial position data frame and portfolio
        df_strategy = pd.DataFrame(data=None, columns=['Portfolio', 'Transcation', 'Cash', 'Shares'], index=trades.index)
        df_strategy.loc[trades.index[0],'Transcation'] = 0
        df_strategy.loc[trades.index[0],'Shares'] = 0
        df_strategy.loc[trades.index[0],'Cash'] = sv
        df_strategy.loc[trades.index[0], 'Portfolio'] = sv

        ## simulate portfolio value
        for ii in range(1, len(df_strategy)):
            ## prior date index
            yesterday = df_strategy.index[(ii) - 1]
            ## get date
            today = df_strategy.index[ii]
            if (BBands.loc[today,'Signal'] == 1) or (SKD.loc[today,'Signal'] == 1) or (RSI_Results.loc[today,'Signal'] == 1):
                ## check position
                if df_strategy.loc[yesterday,'Shares'] != 1000:
                    ## update transcation number
                    df_strategy.loc[today, 'Shares'] = 1000
                    df_strategy.loc[today, 'Transcation'] = 1000 - df_strategy.loc[yesterday, 'Shares']
                    ## historical price
                    stock_price = trades.loc[today,symbol]

                    ## calcualate cash
                    transcation_cost = Commission +  np.abs(stock_price * df_strategy.loc[today, 'Transcation'] * impact)
                    df_strategy.loc[today, 'Cash'] = (df_strategy.loc[yesterday, 'Cash']
                                                      -stock_price*df_strategy.loc[today, 'Transcation']-transcation_cost)
                    df_strategy.loc[today, 'Portfolio'] =  df_strategy.loc[today, 'Cash'] + stock_price*1000
                else:
                    df_strategy.loc[today, 'Shares'] = 1000
                    df_strategy.loc[today, 'Transcation'] = 0
                    ## historical price
                    stock_price = trades.loc[today, symbol]
                    ## calcualate cash
                    df_strategy.loc[today, 'Cash'] = df_strategy.loc[yesterday, 'Cash']
                    df_strategy.loc[today, 'Portfolio'] = df_strategy.loc[today, 'Cash'] + stock_price * 1000
            ## short position
            elif (BBands.loc[today,'Signal'] == -1) or (SKD.loc[today,'Signal'] == -1) or (RSI_Results.loc[today,'Signal'] == -1):


                ## check position
                if df_strategy.loc[yesterday, 'Shares'] != -1000:
                    ## update transcation number
                    df_strategy.loc[today, 'Shares'] = -1000
                    df_strategy.loc[today, 'Transcation'] = -1000 - df_strategy.loc[yesterday, 'Shares']
                    ## historical price
                    stock_price = trades.loc[today, symbol]

                    ## calcualate cash
                    transcation_cost = Commission + np.abs(stock_price * df_strategy.loc[today, 'Transcation'] * impact)
                    df_strategy.loc[today, 'Cash'] = (df_strategy.loc[yesterday, 'Cash']
                                                      - stock_price * df_strategy.loc[
                                                          today, 'Transcation'] - transcation_cost)
                    df_strategy.loc[today, 'Portfolio'] = df_strategy.loc[today, 'Cash'] - stock_price * 1000
                else:
                    df_strategy.loc[today, 'Shares'] = -1000
                    df_strategy.loc[today, 'Transcation'] = 0
                    ## historical price
                    stock_price = trades.loc[today, symbol]
                    ## calcualate cash
                    df_strategy.loc[today, 'Cash'] = df_strategy.loc[yesterday, 'Cash']
                    df_strategy.loc[today, 'Portfolio'] = df_strategy.loc[today, 'Cash'] - stock_price * 1000
            ## keep portfolio as it is
            else:
                df_strategy.loc[today, 'Shares'] = df_strategy.loc[yesterday, 'Shares']
                df_strategy.loc[today, 'Transcation'] = 0
                ## historical price
                stock_price = trades.loc[today, symbol]
                ## calcualate cash
                df_strategy.loc[today, 'Cash'] = df_strategy.loc[yesterday, 'Cash']
                df_strategy.loc[today, 'Portfolio'] = df_strategy.loc[yesterday, 'Shares']*stock_price+df_strategy.loc[today, 'Cash']
        self.df_strategy = df_strategy
        df_trades = pd.DataFrame(data=df_strategy['Transcation'].values, columns= ['Transcation'],index= df_strategy.index)
        return  df_trades

if __name__ == "__main__":
    obj = ManualStrategy()
    df_trades = obj.testPolicy(
            symbol="JPM",
            sd=dt.datetime(2008, 1, 1),
            ed=dt.datetime(2009, 12, 31),
            sv=100000)
