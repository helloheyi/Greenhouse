import pandas as pd
from util import get_data
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import warnings
warnings.filterwarnings("ignore")
def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "yhe600"  # replace tb34 with your Georgia Tech username
def chart(df,df_benchmark):
    ## normalized to 1.0
    df = df/df.iloc[0,0]
    df_benchmark = df_benchmark/df_benchmark.iloc[0,0]
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.plot(df.index, df['Portfolio'], label="Theoretically Optimal Portfolio", linestyle="-",color='red')
    ax.plot(df.index, df_benchmark['Portfolio'], label="Benchmark", linestyle="-",color='purple')
    ax.set_xlabel("Date")
    ax.set_ylabel("Normalized Value")
    ax.legend()
    ax.set_title("Figure 1: Comparison between benchmark and optimal portfolio")
    ax.set_xlim(df.index[0], df.index[-1])

    # Use DateFormatter to format the x-axis
    date_format = mdates.DateFormatter('%Y-%m')
    ax.xaxis.set_major_formatter(date_format)
    # Optionally, rotate the x-axis labels for better readability
    plt.xticks(rotation=45)
    # Add grid lines
    ax.grid(True)
    plt.savefig('TOP.png')

    plt.close()

def stat(df,df_benchmark):
    df_performance = pd.DataFrame(data = None, columns = ['Benchmark','Portfolio'],
                                  index = ['Cumulative return','StDev of daily returns','Mean of daily returns'])

    def daily(df):
        cr = df[-1] / df[0]-1
        sd = (df.shift(-1)/df-1).std()
        mean= (df.shift(-1)/df-1).mean()
        return [cr,sd,mean]

    port_list = ['Benchmark','Portfolio']
    per_ben = daily(df_benchmark['Portfolio'])
    df_performance['Benchmark'] = per_ben
    per_port = daily(df['Portfolio'])
    df_performance['Portfolio'] = per_port
    sr = np.sqrt(252)*((per_port[2]-per_ben[2])/per_port[1])
    df_performance['Sharp Ratio'] = sr
    return df_performance

def testPolicy(symbol,sd,ed,sv):
    ##start value
    start_value = sv
    start_date = sd
    end_date = ed
    ## get price --please use adj close price to eval portfolio
    price = get_data([symbol], pd.date_range(start_date, end_date)).astype(float)

    ## forward then back fill na
    price = price.fillna(method='ffill')
    price = price.fillna(method='bfill')
    ## remove
    ## benchmark --- 1000 shares
    df_Benchmark = pd.DataFrame(data=None, columns= ['Portfolio'], index= price.index)
    price_index = price.index

    rest_cash = sv - 1000*price.loc[price_index[0], symbol]
    df_Benchmark['Portfolio'] = 1000*price[symbol] + rest_cash

    ## test strategy
    # Allowable positions are 1000 shares long, 1000 shares short, 0 shares.
    # (You may trade up to 2000 shares at a time as long as your positions are 1000 shares long or 1000 shares short.)
    df_strategy = pd.DataFrame(data = None, columns= ['Portfolio','Values','Cash','Shares'] , index= price.index)
    ## create t1 portfoilo
    if price.loc[price_index[1],symbol] > price.loc[price_index[0],symbol]:
    #
        # long 1000 as initial position
        df_strategy.loc[price_index[0],'Values'] = 1000
        df_strategy.loc[price_index[0], 'Portfolio'] = sv
        df_strategy.loc[price_index[0], 'Cash'] = rest_cash
        df_strategy.loc[price_index[0], 'Shares'] = 1000
    elif price.loc[price_index[1],symbol] == price.loc[price_index[0],symbol]:
        ## do nothing
        df_strategy.loc[price_index[0],'Values'] = 0
        df_strategy.loc[price_index[0], 'Portfolio'] = sv
        df_strategy.loc[price_index[0], 'Cash'] = sv
        df_strategy.loc[price_index[0], 'Shares'] = 0

    else:
        ## short -1000 as initial position
        df_strategy.loc[price_index[0],'Values'] = -1000
        df_strategy.loc[price_index[0], 'Portfolio'] = sv
        df_strategy.loc[price_index[0], 'Cash'] = sv - (-1000)*price.loc[price_index[0],symbol]
        df_strategy.loc[price_index[0], 'Shares'] = -1000
    #
    for ii in range (1,len(df_strategy)-1):
        ### take long 1000
        if price.loc[price_index[ii+1],symbol] > price.loc[price_index[(ii)],symbol]:
            ## Allowable positions are 1000 shares long, 1000 shares short, 0 shares.
            if df_strategy.loc[price_index[(ii-1)],'Shares'] != 1000:
                df_strategy.loc[price_index[ii], 'Shares'] =1000
                df_strategy.loc[price_index[ii], 'Values'] = 1000 - df_strategy.loc[price_index[(ii-1)],'Shares']
                df_strategy.loc[price_index[ii], 'Cash'] = df_strategy.loc[price_index[(ii-1)], 'Cash'] - df_strategy.loc[price_index[ii], 'Values']*price.loc[price_index[ii], symbol]
                df_strategy.loc[price_index[ii], 'Portfolio'] = df_strategy.loc[price_index[ii], 'Cash'] + df_strategy.loc[price_index[ii], 'Shares']*price.loc[price_index[ii], symbol]

            else:
                df_strategy.loc[price_index[ii], 'Values'] = 0
                df_strategy.loc[price_index[ii], 'Cash'] = df_strategy.loc[price_index[(ii - 1)], 'Cash']
                df_strategy.loc[price_index[ii], 'Shares'] = df_strategy.loc[price_index[(ii - 1)], 'Shares']
                df_strategy.loc[price_index[ii], 'Portfolio'] = df_strategy.loc[price_index[ii], 'Cash'] + \
                                                                df_strategy.loc[price_index[ii], 'Shares'] * price.loc[
                                                                    price_index[ii], symbol]

        ## take short postion 1000

        elif price.loc[price_index[(ii+1)],symbol] < price.loc[price_index[ii],symbol]:
            ## Allowable positions are 1000 shares long, 1000 shares short, 0 shares.
            if df_strategy.loc[price_index[(ii-1)],'Shares'] != -1000:
                df_strategy.loc[price_index[ii], 'Shares'] =-1000
                df_strategy.loc[price_index[ii], 'Values'] = -1000 - df_strategy.loc[price_index[(ii-1)],'Shares']

                df_strategy.loc[price_index[ii], 'Cash'] = df_strategy.loc[price_index[(ii-1)], 'Cash'] - df_strategy.loc[price_index[ii], 'Values']*price.loc[price_index[ii], symbol]
                df_strategy.loc[price_index[ii], 'Portfolio'] = df_strategy.loc[price_index[ii], 'Cash'] + df_strategy.loc[price_index[ii], 'Shares']*price.loc[price_index[ii], symbol]

            else:
                df_strategy.loc[price_index[ii], 'Values'] = 0
                df_strategy.loc[price_index[ii], 'Cash'] = df_strategy.loc[price_index[(ii-1)], 'Cash']
                df_strategy.loc[price_index[ii], 'Shares'] = df_strategy.loc[price_index[(ii-1)], 'Shares']
                df_strategy.loc[price_index[ii], 'Portfolio'] = df_strategy.loc[price_index[ii], 'Cash'] + df_strategy.loc[price_index[ii], 'Shares']*price.loc[price_index[ii], symbol]

        else:
            df_strategy.loc[price_index[ii], 'Values'] = 0
            df_strategy.loc[price_index[ii], 'Cash'] = df_strategy.loc[price_index[(ii - 1)], 'Cash']
            df_strategy.loc[price_index[ii], 'Shares'] = df_strategy.loc[price_index[(ii - 1)], 'Shares']
            df_strategy.loc[price_index[ii], 'Portfolio'] = df_strategy.loc[price_index[ii], 'Cash'] + df_strategy.loc[price_index[ii], 'Shares'] * price.loc[price_index[ii], symbol]

   ### last day
    df_strategy.loc[price_index[-1], 'Values'] = 0
    df_strategy.loc[price_index[-1], 'Cash'] = df_strategy.loc[price_index[-2], 'Cash']
    df_strategy.loc[price_index[-1], 'Shares'] = df_strategy.loc[price_index[-2], 'Shares']
    df_strategy.loc[price_index[-1], 'Portfolio'] = df_strategy.loc[price_index[-1], 'Cash'] + df_strategy.loc[price_index[-1], 'Shares'] * price.loc[price_index[-1], symbol]
    ## figure
    chart(df_strategy, df_Benchmark)
    ## performance
    df_performance = stat(df_strategy, df_Benchmark)
    print(df_strategy)
    ##output
    df_trades = df_strategy['Values'].to_frame()
    df_performance.to_csv('Portfolio.csv')


    return df_trades

if __name__ == "__main__":
    df_strategy = testPolicy("JPM",dt.datetime(2008, 1, 1),dt.datetime(2009,12,31),100000)
    # price.to_csv('AAPL.csv')
