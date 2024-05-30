		  	   		  		 		  		  		    	 		 		   		 		    		  	   		  		 		  		  		    	 		 		   		 		  
import random
import BagLearner as bl
import RTLearner as rt
import util as ut
from util import get_data
from indicators import *
import pandas as pd
import datetime as dt

class StrategyLearner(object):  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		  		 		  		  		    	 		 		   		 		  
        If verbose = False your code should not generate ANY output.  		  	   		  		 		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		  		 		  		  		    	 		 		   		 		  
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		  		 		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		  		 		  		  		    	 		 		   		 		  
    :param commission: The commission amount charged, defaults to 0.0  		  	   		  		 		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    # constructor  		  	   		  		 		  		  		    	 		 		   		 		  
    def __init__(self, verbose=False, impact=0.0, commission=0.0):  		  	   		  		 		  		  		    	 		 		   		 		  
        """  		  	   		  		 		  		  		    	 		 		   		 		  
        Constructor method  		  	   		  		 		  		  		    	 		 		   		 		  
        """  		  	   		  		 		  		  		    	 		 		   		 		  
        self.verbose = verbose  		  	   		  		 		  		  		    	 		 		   		 		  
        self.impact = impact  		  	   		  		 		  		  		    	 		 		   		 		  
        self.commission = commission
        self.learner = bl.BagLearner(learner = rt.RTLearner, kwargs = {"leaf_size":10}, bags = 20, boost = False,verbose = self.verbose)
        # self.learner = rt.RTLearner(5, False)

    def author(self):
        return 'yhe600'  # replace tb34 with your Georgia Tech username.

    def target_Y(self,symbol,trades,sv):

        trades['Res'] = ( trades[symbol].shift(-5)  / trades[symbol]  - 1)
        trades['Signal'] = 0
        buy_threshold = 0.02 + self.impact+self.commission/sv
        sell_threshold = -0.02 -self.impact-self.commission/sv
        trades.loc[trades['Res'] > buy_threshold,'Signal'] = 1
        trades.loc[trades['Res'] < sell_threshold,'Signal'] = -1

        self.target = trades
    def sim_Portfolio(self,trades,sv,Target,symbol):
        ## initial position data frame and portfolio
        df_strategy = pd.DataFrame(data=None, columns=['Portfolio', 'Transcation', 'Cash', 'Shares'],
                                   index=trades.index)
        df_strategy.loc[trades.index[0], 'Transcation'] = 0
        df_strategy.loc[trades.index[0], 'Shares'] = 0
        df_strategy.loc[trades.index[0], 'Cash'] = sv
        df_strategy.loc[trades.index[0], 'Portfolio'] = sv
        ## simulate portfolio value
        for ii in range(1, len(df_strategy)):
            ## prior date index
            yesterday = df_strategy.index[(ii) - 1]
            ## get date
            today = df_strategy.index[ii]
            if (Target[ii] == 1):
                ## check position
                if df_strategy.loc[yesterday, 'Shares'] != 1000:
                    ## update transcation number
                    df_strategy.loc[today, 'Shares'] = 1000
                    df_strategy.loc[today, 'Transcation'] = 1000 - df_strategy.loc[yesterday, 'Shares']
                    ## historical price
                    stock_price = trades.loc[today, symbol]

                    ## calcualate cash
                    transcation_cost = self.commission + np.abs(
                        stock_price * df_strategy.loc[today, 'Transcation'] * self.impact)
                    df_strategy.loc[today, 'Cash'] = (df_strategy.loc[yesterday, 'Cash']
                                                      - stock_price * df_strategy.loc[
                                                          today, 'Transcation'] - transcation_cost)
                    df_strategy.loc[today, 'Portfolio'] = df_strategy.loc[today, 'Cash'] + stock_price * 1000
                else:
                    df_strategy.loc[today, 'Shares'] = 1000
                    df_strategy.loc[today, 'Transcation'] = 0
                    ## historical price
                    stock_price = trades.loc[today, symbol]
                    ## calcualate cash
                    df_strategy.loc[today, 'Cash'] = df_strategy.loc[yesterday, 'Cash']
                    df_strategy.loc[today, 'Portfolio'] = df_strategy.loc[today, 'Cash'] + stock_price * 1000
            ## short position
            elif (Target[ii] == -1):

                ## check position
                if df_strategy.loc[yesterday, 'Shares'] != -1000:
                    ## update transcation number
                    df_strategy.loc[today, 'Shares'] = -1000
                    df_strategy.loc[today, 'Transcation'] = -1000 - df_strategy.loc[yesterday, 'Shares']
                    ## historical price
                    stock_price = trades.loc[today, symbol]

                    ## calcualate cash
                    transcation_cost = self.commission + np.abs(
                        stock_price * df_strategy.loc[today, 'Transcation'] * self.impact)
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
                df_strategy.loc[today, 'Portfolio'] = df_strategy.loc[yesterday, 'Shares'] * stock_price + \
                                                      df_strategy.loc[today, 'Cash']

        self.df_strategy = df_strategy
    # this method should create a QLearner, and train it for trading  		  	   		  		 		  		  		    	 		 		   		 		  
    def add_evidence( self,symbol, sd,ed, sv ):
        """
              I will use three indicators loaded from indicators.py
              1. Boollinger_Bands
              2. Stochastic_KD
              3. RSI
              If any selling/buy indicate from the indicators, check the position and do action.
              Equal weighted for these indicators
        """

  		  	   		  		 		  		  		    	 		 		   		 		  
        # add your code to do learning here
        dates = pd.date_range(sd, ed)
        prices_all = get_data([symbol],dates).astype(float)  # automatically adds SPY
        trades = prices_all[[symbol, ]]  # only portfolio symbols
        ## fill na
        trades = trades.fillna(method='ffill')
        trades = trades.fillna(method='bfill')
        ## create the dataset to feed the model
        BBands = Boollinger_Bands(symbol,sd,ed,14,figure= False)
        SKD = Stochastic_KD(symbol, sd,ed, 14, 3, figure= False)
        RSI_Results = RSI(symbol, sd,ed, 14, figure=False)
        ## create target Y
        self.target_Y(symbol, trades, sv)

        df = pd.concat((BBands['Upper_Band'],BBands['Lower_Band'],SKD['%K'],
                SKD['%D'],RSI_Results['RSI'],self.target['Signal']),axis = 1).dropna()
        trainY = df.iloc[:,-1].values
        trainX = np.array(df.iloc[:,:-1])

        if self.verbose == True:
            try:
                self.learner.add_evidence(trainX, trainY)
            except Exception as e:
                print(e)
        else:
            self.learner.add_evidence(trainX, trainY)



    # this method should use the existing policy and test it against new data  		  	   		  		 		  		  		    	 		 		   		 		  
    def testPolicy(  		  	   		  		 		  		  		    	 		 		   		 		  
        self,symbol,sd, ed,sv):
        # add your code to do learning here
        dates = pd.date_range(sd, ed)
        prices_all = get_data([symbol],dates).astype(float)  # automatically adds SPY
        trades = prices_all[[symbol, ]]  # only portfolio symbols
        ## fill na
        trades = trades.fillna(method='ffill')
        trades = trades.fillna(method='bfill')

        ## create the dataset to feed the model
        BBands = Boollinger_Bands(symbol,sd,ed,14,figure= False)
        SKD = Stochastic_KD(symbol, sd,ed, 14, 3, figure= False)
        RSI_Results = RSI(symbol, sd,ed, 14, figure=False)


        df = pd.concat((BBands['Upper_Band'],BBands['Lower_Band'],SKD['%K'],
                SKD['%D'],RSI_Results['RSI']),axis = 1).dropna()

        testX = df.values

        # Querying the learner for testY
        if self.verbose == True:
            try:
                testY = self.learner.query(testX)
            except Exception as e:
                print(e)
        else:
            testY = self.learner.query(testX)
        fillNAtestY = [0] * (len(trades) - len(testY)) + testY
        self.sim_Portfolio(trades, sv, fillNAtestY, symbol)
        df_trades = pd.DataFrame(data=self.df_strategy['Transcation'].values, columns= ['Transcation'],index= self.df_strategy.index)
        return df_trades
  		  	   		  		 		  		  		    	 		 		   		 		  
if __name__ == "__main__":

    symbol = "UNH"
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    dates = pd.date_range(sd, ed)
    prices_all = get_data([symbol], dates).astype(float)  # automatically adds SPY
    trades = prices_all[[symbol, ]]  # only portfolio symbols
    ## fill na
    trades = trades.fillna(method='ffill')
    trades = trades.fillna(method='bfill')
    ## benchmark --- 1000 shares
    df_Benchmark = pd.DataFrame(data=None, columns=['Portfolio'], index=trades.index)
    price_index = trades.index
    Commission = 0
    impact = 0
    sv = 100000
    stock_price = trades.loc[price_index[0], symbol]
    rest_cash = sv - 1000 * trades.loc[price_index[0], symbol] - Commission - np.abs(stock_price * 1000 * impact)
    df_Benchmark['Portfolio'] = 1000 * trades[symbol] + rest_cash
    df_Benchmark['Price'] = trades[symbol]

    ## out sample
    sd = dt.datetime(2010, 1, 1)
    ed = dt.datetime(2011, 12, 31)
    dates = pd.date_range(sd, ed)
    prices_all = get_data([symbol], dates).astype(float)  # automatically adds SPY
    trades = prices_all[[symbol, ]]  # only portfolio symbols
    ## fill na
    trades = trades.fillna(method='ffill')
    trades = trades.fillna(method='bfill')
    ## benchmark --- 1000 shares
    df_Benchmark_Out = pd.DataFrame(data=None, columns=['Portfolio'], index=trades.index)
    price_index = trades.index
    Commission = 0
    impact = 0
    sv = 100000
    stock_price = trades.loc[price_index[0], symbol]
    rest_cash = sv - 1000 * trades.loc[price_index[0], symbol] - Commission - np.abs(stock_price * 1000 * impact)
    df_Benchmark_Out['Portfolio'] = 1000 * trades[symbol] + rest_cash
    df_Benchmark_Out['Price'] = trades[symbol]


    for ii in range(0,100):
        st = StrategyLearner(verbose = False, impact= 0, commission= 0)
        st.add_evidence(symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
        trades = st.testPolicy(symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
        diff = (st.df_strategy['Portfolio'] / 100000)[-1] - (df_Benchmark['Portfolio']/sv)[-1]
        print('In-sample',diff)
        # sd = dt.datetime(2010, 1, 1)
        # ed = dt.datetime(2011, 12, 31)
        # trades = st.testPolicy(symbol, sd=sd, ed=ed, sv=100000)
        # diff = (st.df_strategy['Portfolio'] / 100000)[-1] - (df_Benchmark_Out['Portfolio'] / sv)[-1]
        # print('Out-sample', diff)
        # print(st.df_strategy)








