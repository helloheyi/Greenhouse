""""""
import pandas as pd

"""  		  	   		  		 		  		  		    	 		 		   		 		  
Test a learner.  (c) 2015 Tucker Balch  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		  		 		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		  		 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		  		 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		  		 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 		  		  		    	 		 		   		 		  
or edited.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		  		 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		  		 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		  		 		  		  		    	 		 		   		 		  
"""  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
import math  		  	   		  		 		  		  		    	 		 		   		 		  
import sys
import numpy as np  		  	   		  		 		  		  		    	 		 		   		 		  
import warnings
warnings.filterwarnings("ignore")
import LinRegLearner as lrl
import DTLearner as dt
import RTLearner as rt
import BagLearner as bl
import InsaneLearner as it
import time
import os
import matplotlib.pyplot as plt
import random
import pandas as pd
import scipy.stats

## MEAN absolute error
def MAE(y_true,y_pred):
    result = sum(abs(y_true-y_pred))/len(y_true)
    return result

## R-Squared
def RSquared(y_true,y_pred):
    y_mean = np.ones(len(y_true)) * np.mean(y_true)

    up = np.sum((y_true - y_pred) ** 2)
    down = np.sum((y_true - y_mean) ** 2)
    Result = 1 - up / down
    return Result
## Mean Absolute Percentage Error
def MAPE(y_true,y_pred):
    result = np.sum(abs((y_true - y_pred) / y_true)) / len(y_true)
    return result

## Maximum Error
def ME(y_true,y_pred):
    result = np.max(abs(y_true - y_pred))
    return result

## Root Mean Square Error
def RMSE(y_true,y_pred):
    result = math.sqrt(((y_true - y_pred) ** 2).sum() / len(y_true))
    return result
##
# from datetime import datetime
# start=datetime.now()
#
# #Statements
#
# print datetime.now()-start
#def Time()
## dtlearner
def Experiment1(train_x, train_y, test_x, test_y):
    ## create a dtlearner object
    Insample_lsit = np.array([])
    OutSample_list = np.array([])

    for leaf_size in range(1,len(train_x)):
        leaner = dt.DTLearner(leaf_size,False)
        leaner.add_evidence(train_x, train_y)
        ##in sample analysis
        predY_Insample =leaner.query(train_x)
        ##out sample analysis
        predY_Outsample =leaner.query(test_x)

        Insample = RMSE(train_y,predY_Insample)
        Insample_lsit = np.append(Insample_lsit,Insample)
        OutSample = RMSE(test_y,predY_Outsample)
        OutSample_list = np.append(OutSample_list,OutSample)
    ## check the overfitting point
    for ii in range (0,len(Insample_lsit)):
        if OutSample_list[ii]  == Insample_lsit[ii]:
            point = OutSample_list[ii]

    point_value = [ii, point]
    plt.xlim(1, len(train_x))
    min_ylim = min(np.min(Insample_lsit),np.min(OutSample_list))-0.01
    max_ylim = max(np.max(Insample_lsit),np.max(OutSample_list)) + 0.01
    plt.ylim(min_ylim, max_ylim)
    plt.plot( Insample_lsit, label="In sample RMSE", linestyle="-")
    plt.plot( OutSample_list, label="Out sample RMSE",linestyle="-")
    plt.xlabel("Leaf Size")
    plt.ylabel("RMSE")
    plt.legend()
    # plt.show()
    plt.grid(True)
    plt.title("Experiment1: RMSE respects to Leaf Size for Decision Tree")
    # plt.show()
    plt.savefig(os.path.join(os.path.dirname(__file__), 'images/Figure 1.png'))
    plt.close()

def Experiment2(train_x, train_y, test_x, test_y):
    ## create a dtlearner object
    Insample_lsit = []
    OutSample_list = []
    for leaf_size in range(1,len(train_x)):

        leaner = bl.BagLearner(learner=dt.DTLearner, kwargs={"leaf_size":leaf_size}, bags=5, boost=False, verbose=False)
        leaner.add_evidence(train_x, train_y)
        ##in sample analysis
        predY_Insample =leaner.query(train_x)
        ##out sample analysis
        predY_Outsample =leaner.query(test_x)

        Insample = RMSE(train_y,predY_Insample)
        Insample_lsit.append(Insample)
        OutSample = RMSE(test_y,predY_Outsample)
        OutSample_list.append(OutSample)

    plt.xlim(1, len(train_x))
    min_ylim = min(np.min(Insample_lsit), np.min(OutSample_list)) - 0.01
    max_ylim = max(np.max(Insample_lsit), np.max(OutSample_list)) + 0.01
    plt.ylim(min_ylim, max_ylim)
    plt.plot( Insample_lsit, label="In sample RMSE", linestyle="-")
    plt.plot( OutSample_list, label="Out sample RMSE",linestyle="-")
    plt.grid(True)
    plt.xlabel("Leaf Size")
    plt.ylabel("RMSE")
    plt.legend()
    plt.title("Experiment2: RMSE respects to Leaf Size for Bag with Decision Tree")
    # plt.show()
    plt.savefig(os.path.join(os.path.dirname(__file__), 'images/Figure 2.png'))
    plt.close()

## MAN absolute error
## R-Squared
## first step to select leaf size by MAE
def Experiment3(train_x, train_y, test_x, test_y):
    ## create a dtlearner object
    #MAE
    MAE_DTOutSample = []
    MAE_RTOutSample = []

    for leaf_size in range(1, len(train_x)):
        ## decision tree
        leanerDT = dt.DTLearner(leaf_size,False)
        leanerDT.add_evidence(train_x, train_y)
        ##out sample analysis
        DTpredY_Outsample = leanerDT.query(test_x)
        ## MAE results
        MAE_DTOutSample.append(MAE(test_y, DTpredY_Outsample))

        ## random tree
        leanerRT = rt.RTLearner(leaf_size, False)
        leanerRT.add_evidence(train_x, train_y)
        ##in sample analysis
        ##out sample analysis
        RTpredY_Outsample = leanerRT.query(test_x)
        ## MAE
        MAE_RTOutSample.append(MAE(test_y,RTpredY_Outsample))
        ## Find the index of the min value
    DT_index = np.argmin(MAE_DTOutSample)+1
    RT_index = np.argmin(MAE_RTOutSample)+1

    return DT_index,RT_index


## plot errors histogram
def AnalysisExperiment3(train_x, train_y, test_x, test_y):
    def stat(Error):
        mean = []
        variance = []
        max = []
        skew = []
        kurtosis = []
        for item in Error:
            mean.append(np.mean(item))
            variance.append(np.var(item))
            max.append(np.max(item))
            skew.append(scipy.stats.skew(item))
            kurtosis.append(scipy.stats.kurtosis(item))
        res = np.array((mean,variance,max,skew,kurtosis))
        return res

    ## create a dtlearner object

    ## determine the leaf size
    DT_index, RT_index = Experiment3(train_x, train_y, test_x, test_y)

    index_list = [DT_index, RT_index]
    summary =  locals()
    timeusage_list = ['na','na']
    for ii in range(0,2):
    ## decision tree
        DTstart_time = time.time()
        leanerDT = dt.DTLearner(index_list[ii], False)
        leanerDT.add_evidence(train_x, train_y)
        DTtime_usage = time.time() - DTstart_time
        timeusage_list.append(DTtime_usage)
        ##in sample analysis
        DTpredY_Insample = leanerDT.query(train_x)
        ##out sample analysis
        DTpredY_Outsample = leanerDT.query(test_x)
        ## RSquare results
        RSq_DTInsample = RSquared(train_y, DTpredY_Insample)
        RSq_DTOutsample = RSquared(test_y, DTpredY_Outsample)

        DT_InSample_Error = abs(train_y-DTpredY_Insample)
        DT_OutSample_Error = abs(test_y-DTpredY_Outsample)
        RTstart_time = time.time()
        ## Random tree
        leanerRT = rt.RTLearner(index_list[ii], False)
        leanerRT.add_evidence(train_x, train_y)
        RTtime_usage = time.time() - RTstart_time
        timeusage_list.append(RTtime_usage)
        ##in sample analysis
        RTpredY_Insample = leanerRT.query(train_x)
        ##out sample analysis
        RTpredY_Outsample = leanerRT.query(test_x)
        ## RSquare results
        RSq_RTInsample = RSquared(train_y, RTpredY_Insample)
        RSq_RTOutsample = RSquared(test_y, RTpredY_Outsample)
        RT_InSample_Error = abs(train_y-RTpredY_Insample)
        RT_OutSample_Error = abs(test_y-RTpredY_Outsample)
        ## stats
        Error = [DT_InSample_Error,DT_OutSample_Error,RT_InSample_Error,RT_OutSample_Error]
        RSquare = np.array([RSq_DTInsample,RSq_DTOutsample,RSq_RTInsample,RSq_RTOutsample])
        res = np.append(stat(Error),RSquare).reshape((6, 4))
        summary["df{}".format(ii)] = pd.DataFrame(data = res,
                                                  columns =['DT_InSample_Error.{}'.format(ii),'DT_OutSample_Error.{}'.format(ii),
                                                            'RT_InSample_Error.{}'.format(ii),'RT_OutSample_Error.{}'.format(ii)],
                                                  index=['mean','variance','max','skew','kurtosis','RSquare'])

        plt.hist(DT_OutSample_Error, bins=int(len(test_y) / 5), color='blue',label='Decision Tree Out Sample Errors')
        plt.hist(RT_OutSample_Error, bins=int(len(test_y) / 5), color='red',label='Random Tree Out Sample Errors')
        plt.xlabel('Error')
        plt.ylabel('Frequency')
        plt.legend()
        leaf_size = index_list[ii]
        plt.title('Decision Tree vs Random Tree for Errors with leaf size {}'.format(leaf_size))
        plt.savefig(os.path.join(os.path.dirname(__file__), 'images/Figure {}.png'.format(ii+3)))
        plt.close()

        plt.hist(DT_InSample_Error, bins=int(len(test_y) / 5), color='blue',label='Decision Tree in Sample Errors')
        plt.hist(RT_InSample_Error, bins=int(len(test_y) / 5), color='red',label='Random Tree In Sample Errors')
        plt.xlabel('Error')
        plt.xlabel('Error')
        plt.ylabel('Frequency')
        plt.legend()
        plt.title('Decision Tree vs Random Tree for Errors with leaf size {}'.format(leaf_size))
        plt.savefig(os.path.join(os.path.dirname(__file__), 'images/Figure {}.png'.format(ii+5)))
        plt.close()
    df_Final  = pd.concat([summary["df{}".format(0)],summary["df{}".format(1)]],axis = 1)
    df_Final['Time Usage'] = timeusage_list

    df_Final.to_csv('Experiment 3 result.txt')

def test(train_x, train_y, test_x, test_y):
    # Experiment1(train_x, train_y, test_x, test_y)
    # Experiment2(train_x, train_y, test_x, test_y)
    AnalysisExperiment3(train_x, train_y, test_x, test_y)





if __name__ == "__main__":  		  	   		  		 		  		  		    	 		 		   		 		  
    # if len(sys.argv) != 2:
    #     print("Usage: python testlearner.py <filename>")
    #     sys.exit(1)
    # inf = open(sys.argv[1])
    # data = np.array(
    #     [list(map(float, s.strip().split(","))) for s in inf.readlines()]
    # )
  		  	   		  		 		  		  		    	 		 		   		 		  
    # compute how much of the data is training and testing

    alldata = np.genfromtxt(os.path.join(os.path.dirname(__file__), 'Data/Istanbul.csv'), delimiter=",")
    data = alldata[1:, 1:]
    Size = int(len(data) * 0.6)
    TrainData = np.array(random.choices(data, k=Size))
    train_x = TrainData[:, 0:-1]
    train_y = TrainData[:, -1]
    testData = np.array([i for i in data if i not in TrainData])
    test_x = testData[:, 0:-1]
    test_y = testData[:, -1]
    start_time = time.time()
    test(train_x, train_y, test_x, test_y)
