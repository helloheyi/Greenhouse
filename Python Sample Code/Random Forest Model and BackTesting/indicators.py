
def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "yhe600"  # replace tb34 with your Georgia Tech username
##3 simple moving average
def SMA(symbol,start_date,end_date,windown_size):
    ## simple moving average with in windown_size
    price = get_data([symbol], pd.date_range(start_date, end_date)).astype(float)

    ## forward then back fill na
    price = price.fillna(method='ffill')
    price = price.fillna(method='bfill')
    df = price[symbol].to_frame()
    df['SMA'] = df[symbol].rolling(window=windown_size).mean()
    return df

def Boollinger_Bands(symbol,start_date,end_date,windown_size,figure= False):
     ## three lines upper bound (SMA (simple moving average) + 2*standard deviations), lower bound  (SMA - 2*standard deviations) and mean
    df =  SMA(symbol,start_date,end_date,windown_size)
    df['Upper_Band'] = df['SMA'] +2*df[symbol].rolling(window=windown_size).std()
    df['Lower_Band'] = df['SMA'] - 2*df[symbol].rolling(window=windown_size).std()
    df = df / df.loc[df.index[0], symbol]
    df['Signal'] = 0
    ## sell signal -- remove noise
    df.loc[df[symbol] >  (1.02*df['Upper_Band']),'Signal'] = -1
    ## buy signal-- remove noise
    df.loc[df[symbol] < (0.98*df['Lower_Band']), 'Signal'] = 1
    if figure == True:
        df = df.dropna()
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot(df.index, df[symbol], label=symbol, linestyle="-", color='purple')
        ax.plot(df.index, df['SMA'], label='SMA', linestyle="-", color='orange')
        ax.plot(df.index, df['Upper_Band'], label='Upper_Band', linestyle="-", color='b', linewidth=1)
        ax.plot(df.index, df['Lower_Band'], label='Lower_Band', linestyle="-", color='b', linewidth=1)
        ax.fill_between(df.index, df['Lower_Band'], df['Upper_Band'], color='lightgray', alpha=0.5)

        # Add buy (green) and sell (red) signals
        ax.scatter(df.loc[df['Signal'] == 1].index, df.loc[df['Signal'] == 1][symbol], color='g', marker='^',
                   label='Buy Signal', s=100)
        ax.scatter(df.loc[df['Signal'] == -1].index, df.loc[df['Signal'] == -1][symbol], color='r', marker='v',
                   label='Sell Signal', s=100)

        ax.set_xlim(df.index[0], df.index[-1])
        ax.set_xlabel("Date")
        ax.set_ylabel("Normalized Value")
        ax.legend()
        ax.set_title(symbol + " with Bollinger Bands and Signals")
        ax.set_xlim(df.index[0], df.index[-1])

        # Use DateFormatter to format the x-axis
        date_format = mdates.DateFormatter('%Y-%m')
        ax.xaxis.set_major_formatter(date_format)
        plt.xticks(rotation=45)
        # Add grid lines
        ax.grid(True)
        plt.savefig('Bollinger Bands.png')
        plt.close()
    return df

####  Golden Cross
def Cross(symbol,start_date,end_date,windown_size1,windown_size2,figure):
    ## simple moving average with in windown_size 1
    SMA1 = SMA(symbol,start_date,end_date,windown_size1)
    ## simple moving average with in windown_size 2
    SMA2 = SMA(symbol,start_date,end_date,windown_size2)
    df = pd.DataFrame(data =None, columns= ['short-term','long-term',symbol],index  = SMA1.index)
    if windown_size1 > windown_size2:
        df['long-term'] =  SMA1['SMA']
        df['short-term'] = SMA2['SMA']
    else:
        df['long-term'] = SMA2['SMA']
        df['short-term'] = SMA1['SMA']
    df[symbol] = SMA2[symbol]
    ## normalize
    df = df / df.loc[df.index[0], symbol]

    # Detect Golden Cross and Death Cross
    index = df.index
    df['Golden_Cross'] = 0
    for ii in range(1,len(index)):
        ## need to reduce noise
        if df.loc[index[ii],'short-term'] > df.loc[index[ii],'long-term'] and df.loc[index[ii-1],'short-term'] < df.loc[index[ii-1],'long-term']:
            df.loc[index[ii],'Golden_Cross'] =1
        elif df.loc[index[ii],'short-term'] < df.loc[index[ii],'long-term'] and df.loc[index[ii-1],'short-term'] > df.loc[index[ii-1],'long-term']:
            df.loc[index[ii], 'Golden_Cross'] = -1

    if figure == True:
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot(df.index, df[symbol], label=symbol, linestyle="-", color='orange')
        ax.plot(df.index, df['long-term'], label='Long-term SMA', linestyle="-", color='purple', linewidth=0.8)
        ax.plot(df.index, df['short-term'], label='Short-term SMA', linestyle="-", color='blue', linewidth=0.8)
        # Plot Golden Cross and Death Cross

        ax.scatter(df.loc[df['Golden_Cross'] == 1].index, df.loc[df['Golden_Cross'] == 1]['long-term'], color='g', marker='^',
                   label='Golden Cross', s=100)
        ax.scatter(df.loc[df['Golden_Cross'] == -1].index, df.loc[df['Golden_Cross'] == -1]['long-term'], color='r', marker='v',
                   label='Death Cross', s=100)

        ax.set_xlim(df.index[0], df.index[-1])
        ax.set_xlabel("Date")
        ax.set_ylabel("Normalized Value")
        ax.legend()
        ax.set_title('Moving average {}, {} with cross signals'.format(windown_size1, windown_size2))
        ax.set_xlim(df.index[0], df.index[-1])

        # Use DateFormatter to format the x-axis
        date_format = mdates.DateFormatter('%Y-%m')
        ax.xaxis.set_major_formatter(date_format)
        plt.xticks(rotation=45)
        # Add grid lines
        ax.grid(True)
        plt.savefig('cross signals.png')
        # plt.show()
        plt.close()

    return df
#### Stochastic Indicator
def Stochastic_KD(symbol,start_date,end_date,windown_size1,windown_size2,figure):
    ## specified price range for %K in windown_size1
    price_High = get_data([symbol], pd.date_range(start_date, end_date),colname="High")
    price_Low = get_data([symbol], pd.date_range(start_date, end_date),colname="Low")
    price_Close = get_data([symbol], pd.date_range(start_date, end_date),colname="Close")
    df = pd.DataFrame()
    df[symbol] = price_Close[symbol]
    df['High'] = price_High[symbol]
    df['Low'] = price_Low[symbol]
    df['Highest'] = df['High'].rolling(window=windown_size1).max()
    df['Lowest'] = df['Low'].rolling(window=windown_size1).min()
    df['%K'] = (df[symbol] - df['Lowest'])/(df['Highest'] - df['Lowest'])*100
    #simple moving average '%K' with in windown_size2
    df['%D'] =  df['%K'].rolling(window=windown_size2).mean()
    if figure == True:
        ## normalized price
        df = df.dropna()
        df[symbol] = df[symbol] / df.loc[df.index[0], symbol]
        # Create a figure with subplots
        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))
        # # Subplot 1: Price Change
        ax[0].plot(df.index, df[symbol], linestyle="-", color='b')
        ax[0].scatter(df[df['%D'] > 85].index, df[df['%D'] > 85][symbol], color='r', marker='^',
                   label='Sell Signal', s=20)
        ax[0].scatter(df[df['%D'] < 15].index, df[df['%D'] < 15][symbol], color='g', marker='o',
                   label='Buy Signal', s=20)
        ax[0].set_ylabel("Normalized Value")
        ax[0].grid(True)
        ax[0].set_title('Stochastic Oscillator {}, {} with Price Movement'.format(windown_size1, windown_size2))
        ax[0].legend(fontsize='xx-small')

        ## Subplot 2: Stochastic Oscillator
        ax[1].plot(df.index, df['%K'], linestyle="-", color='blue',label='%K',linewidth=1)
        ax[1].plot(df.index, df['%D'], linestyle="-", color='orange',label='%D',linewidth=1)
        ax[1].axhline(y=80, color='red', linestyle='--', label='Overbought > 80',linewidth=0.8)
        ax[1].axhline(y=20, color='green', linestyle='--', label='Oversold < 20',linewidth=0.8)
        ax[1].fill_between(df.index, 20, 80, color='lightgray', alpha=0.5)
        ax[1].fill_between(df.index, df['%K'], 20, where=(df['%K'] < 20),color='lightgreen', alpha=0.5,
                           label='Oversold Area')
        ax[1].fill_between(df.index, df['%K'], 80, where=(df['%K'] > 80),color='lightcoral', alpha=0.5,
                           label='Overbought Area')
        ax[1].set_xlim(df.index[0], df.index[-1])
        ax[1].set_ylim(0, 100)

        ax[1].set_xlabel("Date")
        ax[1].set_ylabel("Stochastic Oscillator")
        ax[1].grid(True)
        ax[1].legend(fontsize='xx-small')
        plt.savefig('Stochastic Oscillator.png')
        plt.close()
    return df

### Rate of Change indicator,
def ROC(symbol,start_date,end_date,windown_size1,windown_size2,windown_size3, figure):
    ## simple moving average with in windown_size
    ##Rate of change (ROC) refers to how quickly something changes over time.
    df = Cross(symbol, start_date, end_date, windown_size1, windown_size2, figure)

    df['ROC'] = (df[symbol]/ df[symbol].shift(windown_size3)-1)*100
    df['Signal'] = 0
    index = df.index
    for ii in range(1, len(index)):
        ## need to reduce noise
        if df.loc[index[ii], 'ROC'] > 1 and df.loc[index[ii - 1], 'ROC'] < 0 and df.loc[index[ii], 'short-term'] > df.loc[index[ii], 'long-term']:
            df.loc[index[ii], 'Signal'] = 1
        elif df.loc[index[ii], 'ROC'] < -1 and df.loc[index[ii - 1], 'ROC'] > 0 and df.loc[index[ii], 'short-term'] < df.loc[index[ii], 'long-term']:
            df.loc[index[ii], 'Signal'] = -1


    if figure == True:
        ## normalized price
        df = df.dropna()

        # Create a figure with subplots
        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))
        # # Subplot 1: Price Change
        ax[0].plot(df.index, df[symbol], label=symbol, linestyle="-", color='orange')
        ax[0].plot(df.index, df['long-term'], label='Long-term SMA', linestyle="-", color='purple', linewidth=0.8)
        ax[0].plot(df.index, df['short-term'], label='Short-term SMA', linestyle="-", color='blue', linewidth=0.8)

        ax[0].set_ylabel("Normalized Value")
        ax[0].set_title(symbol + "Rate of Change (ROC) with Cross Indictor")

        ax[0].scatter(df.loc[df['Signal'] == 1].index, df.loc[df['Signal'] == 1][symbol], color='g',
                   marker='^', label='Buy Signal', s=50)
        ax[0].scatter(df.loc[df['Signal'] == -1].index, df.loc[df['Signal'] == -1][symbol], color='r',
                   marker='v', label='Sell Signal', s=50)
        ax[0].grid(True)
        ax[0].set_xlim(df.index[0], df.index[-1])

        ax[0].legend(fontsize='xx-small')
        ## Subplot 2: Stochastic Oscillator
        ax[1].axhline(y=0, color='r', linestyle='--', linewidth=0.8)

        ax[1].plot(df.index, df['ROC'], linestyle="-", color='orange', label='ROC', linewidth=1)
        ax[1].set_xlim(df.index[0], df.index[-1])
        ax[1].set_xlabel("Date")
        ax[1].set_ylabel("ROC")
        ax[1].grid(True)
        ax[1].legend(fontsize='xx-small')
        plt.savefig('ROC.png')
        plt.close()
    return df

def RSI(symbol,start_date,end_date,windown_size,figure= False):
    ## price difference
    price = get_data([symbol], pd.date_range(start_date, end_date),colname="Close").astype(float)

    ## forward then back fill na
    price = price.fillna(method='ffill')
    price = price.fillna(method='bfill')
    df = price[symbol].to_frame()
    ## daily price changes
    df['Price Change'] = (df[symbol].diff())
    df = df.dropna()
    ## Identify gain
    df['Gain'] =  0
    gain_index  = df[df['Price Change']>0].index
    df.loc[gain_index,'Gain'] =  df.loc[gain_index,'Price Change']
    ## Identify loss
    df['Loss'] =  0
    loss_index  = df[df['Price Change']<0].index
    df.loc[loss_index,'Loss'] = abs(df.loc[loss_index,'Price Change'])
    # Calculate the average gain and average loss over the RSI period
    df['Avg Gain'] = 0
    df['Avg Loss'] = 0
    AG_list = [0] * len(df)
    AL_list = [0] * len(df)
    index_list = df.index
    AG_list[windown_size-1] =  df.loc[:index_list[windown_size-1],'Gain'].mean()
    AL_list[windown_size-1] =  df.loc[:index_list[windown_size-1],'Loss'].mean()
    # df.loc[index_list[windown_size-1],'Avg Loss'] = df.loc[:index_list[windown_size+1],'Loss'].mean()

    for i in range(windown_size, len(df)):
        gain = df.loc[index_list[i],'Gain']
        loss = df.loc[index_list[i],'Loss']
        avg_gain = ((AG_list[i-1] * (windown_size - 1)) + gain) / windown_size
        avg_loss = ((AL_list[i-1] * (windown_size - 1)) + loss) / windown_size
        AG_list[i] = avg_gain
        AL_list[i] = avg_loss
    # Calculate the Relative Strength (RS) and RSI

    df['Avg Gain'] = AG_list
    df['Avg Loss'] = AL_list

    df['RSI'] = 100 - (100/(1+df['Avg Gain']/df['Avg Loss']))

    if figure == True:
        ## normalized price
        df = df.dropna()
        df[symbol] = df[symbol] / df.loc[df.index[0], symbol]

        # Create a figure with subplots
        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))
        # # Subplot 1: Price Change
        ax[0].plot(df.index, df[symbol], linestyle="-", color='b')
        ax[0].scatter(df[df['RSI'] > 70].index, df[df['RSI'] > 70][symbol], color='r', marker='^',
                   label='Sell Signal', s=50)
        ax[0].scatter(df[df['RSI'] < 30].index, df[df['RSI'] < 30][symbol], color='g', marker='o',
                   label='Buy Signal', s=50)
        ax[0].set_ylabel("Normalized Value")
        ax[0].set_title(symbol + " with RSI")
        ax[0].grid(True)
        ax[0].set_xlim(df.index[0], df.index[-1])
        ax[0].legend(fontsize='xx-small')
        ## Subplot 2: RSI
        ax[1].plot(df.index, df['RSI'], linestyle="-", color='orange')
        ax[1].axhline(y=70, color='grey', linestyle='--',label ='Overbought >70')
        ax[1].axhline(y=30, color='grey', linestyle='--',label ='Oversold <30')
        ax[1].fill_between(df.index, 30, 70, color='lightgray', alpha=0.5)
        ax[1].fill_between(df.index, df['RSI'], 30, where=(df['RSI'] < 30),color='green', alpha=1,
                           label='Oversold Area')
        ax[1].fill_between(df.index, df['RSI'], 70, where=(df['RSI'] > 70),color='red', alpha=1,
                           label='Overbought Area')

        # here we use the where argument to only fill the region where the
        ax[1].set_xlim(df.index[0], df.index[-1])
        ax[1].set_xlabel("Date")
        ax[1].set_ylabel("RSI")
        ax[1].grid(True)
        ax[1].legend(fontsize='xx-small')
        ax[1].set_ylim(0, 100)

        plt.savefig('RSI.png')
        plt.close()
    return df


def RSI_update(symbol,start_date,end_date,windown_size,figure= False):
    ## price difference
    price = get_data([symbol], pd.date_range(start_date, end_date),colname="Close").astype(float)

    ## forward then back fill na
    price = price.fillna(method='ffill')
    price = price.fillna(method='bfill')
    df = price[symbol].to_frame()
    ## daily price changes
    df['Price Change'] = (df[symbol].diff())
    df = df.dropna()
    ## Identify gain
    df['Gain'] =  0
    gain_index  = df[df['Price Change']>0].index
    df.loc[gain_index,'Gain'] =  df.loc[gain_index,'Price Change']
    ## Identify loss
    df['Loss'] =  0
    loss_index  = df[df['Price Change']<0].index
    df.loc[loss_index,'Loss'] = abs(df.loc[loss_index,'Price Change'])
    # Calculate the average gain and average loss over the RSI period
    df['Avg Gain'] = df['Gain'].rolling(window=windown_size).mean()
    df['Avg Loss'] = df['Loss'].rolling(window=windown_size).mean()

    # AG_list = [0] * len(df)
    # AL_list = [0] * len(df)
    # index_list = df.index
    # AG_list[windown_size-1] =  df.loc[:index_list[windown_size-1],'Gain'].mean()
    # AL_list[windown_size-1] =  df.loc[:index_list[windown_size-1],'Loss'].mean()
    # # df.loc[index_list[windown_size-1],'Avg Loss'] = df.loc[:index_list[windown_size+1],'Loss'].mean()
    #
    # for i in range(windown_size, len(df)):
    #     gain = df.loc[index_list[i],'Gain']
    #     loss = df.loc[index_list[i],'Loss']
    #     avg_gain = ((AG_list[i-1] * (windown_size - 1)) + gain) / windown_size
    #     avg_loss = ((AL_list[i-1] * (windown_size - 1)) + loss) / windown_size
    #     AG_list[i] = avg_gain
    #     AL_list[i] = avg_loss
    # # Calculate the Relative Strength (RS) and RSI
    #
    # df['Avg Gain'] = AG_list
    # df['Avg Loss'] = AL_list

    df['RSI'] = 100 - (100/(1+df['Avg Gain']/df['Avg Loss']))

    if figure == True:
        ## normalized price
        df = df.dropna()
        df[symbol] = df[symbol] / df.loc[df.index[0], symbol]

        # Create a figure with subplots
        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))
        # # Subplot 1: Price Change
        ax[0].plot(df.index, df[symbol], linestyle="-", color='b')
        ax[0].scatter(df[df['RSI'] > 70].index, df[df['RSI'] > 70][symbol], color='r', marker='^',
                   label='Sell Signal', s=50)
        ax[0].scatter(df[df['RSI'] < 30].index, df[df['RSI'] < 30][symbol], color='g', marker='o',
                   label='Buy Signal', s=50)
        ax[0].set_ylabel("Normalized Value")
        ax[0].set_title(symbol + " with RSI")
        ax[0].grid(True)
        ax[0].set_xlim(df.index[0], df.index[-1])
        ax[0].legend(fontsize='xx-small')
        ## Subplot 2: RSI
        ax[1].plot(df.index, df['RSI'], linestyle="-", color='orange')
        ax[1].axhline(y=70, color='grey', linestyle='--',label ='Overbought >70')
        ax[1].axhline(y=30, color='grey', linestyle='--',label ='Oversold <30')
        ax[1].fill_between(df.index, 30, 70, color='lightgray', alpha=0.5)
        ax[1].fill_between(df.index, df['RSI'], 30, where=(df['RSI'] < 30),color='lightgreen', alpha=0.5,
                           label='Oversold Area')
        ax[1].fill_between(df.index, df['RSI'], 70, where=(df['RSI'] > 70),color='lightcoral', alpha=0.5,
                           label='Overbought Area')

        # here we use the where argument to only fill the region where the
        ax[1].set_xlim(df.index[0], df.index[-1])
        ax[1].set_xlabel("Date")
        ax[1].set_ylabel("RSI")
        ax[1].grid(True)
        ax[1].legend(fontsize='xx-small')
        plt.savefig('RSI update.png')
        plt.close()
    return df


if __name__ == "__main__":
    # Cross("JPM",dt.datetime(2008, 1, 1),
    #                                dt.datetime(2009,12,31),50,15,True)
    # # print(df_strategy)
    # Boollinger_Bands("JPM",dt.datetime(2008, 1, 1),
    #                                 dt.datetime(2009,12,31),10,figure= False)
    # Stochastic_KD("JPM",dt.datetime(2008, 1, 1),
    #                                dt.datetime(2009,12,31),14,3,True)
    # ROC("JPM",dt.datetime(2008, 1, 1),dt.datetime(2009,12,31),5,50,20, True)

    RSI("JPM",dt.datetime(2008, 1, 1),dt.datetime(2009,12,31),14,True)
    # RSI_update("JPM", dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31), 14, True)