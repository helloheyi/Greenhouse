""""""
import pandas as pd

"""  		  	   		  		 		  		  		    	 		 		   		 		  
A simple wrapper for linear regression.  (c) 2015 Tucker Balch  		  	   		  		 		  		  		    	 		 		   		 		  

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

import numpy as np
import os
import sys
import warnings
warnings.filterwarnings("ignore")
import LinRegLearner as lrl
import DTLearner as dt
import RTLearner as rt
import BagLearner as bl
import pandas as pd
import random
import InsaneLearner as it
import time
class BagLearner(object):
    """
    This is a bootstrap Learner. It is implemented correctly.

    :param verbose: If “verbose” is True, your code can print out information for debugging.
        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.
    :type verbose: bool
    """

    def __init__(self, learner=None, kwargs=None, bags=1, boost=False, verbose=False):
        """
        Constructor method
        """

        ### check BagLearner
        
        while len(kwargs.keys()) >3:
            learner = kwargs['learner']
            bags = kwargs['bags'] * bags
            kwargs = kwargs['kwargs']
        self.verbose = verbose

        ## I want to learn how to make it more arbitrarily
        if (str(learner).split("'")[1] == "RTLearner.RTLearner") or (str(learner).split("'")[1] == "DTLearner.DTLearner"):
            kwargs = {'leaf_size':kwargs['leaf_size'],'verbose':self.verbose}
        elif (str(learner).split("'")[1] == "InsaneLearner.InsaneLearner"):
            kwargs = {'verbose': self.verbose}
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost

    def author(self):
        """
        :return: The GT username of the student
        :rtype: str
        """
        return "yhe600"  # replace tb34 with your Georgia Tech username

    def add_evidence(self, data_x, data_y):
        """
        Add training data to learner

        :param data_x: A set of feature values used to train the learner
        :type data_x: numpy.ndarray
        :param data_y: The value we are attempting to predict given the X data
        :type data_y: numpy.ndarray
        """
        ## assume 60% data as subdata
        ## set up data
        ## create a number of bags
        def build_instance(data_x,data_y):
            instance_list = []
            for ii in range(0, self.bags):
                data = np.insert(data_x, 0, data_y, axis=1)
                subSize = int(len(data_x) * 0.6)
                subData = np.array(random.choices(data, k=subSize))
                sub_x = subData[:, 1:]
                sub_y = subData[:, 0]
                obj = self.learner(**self.kwargs)
                # if len(self.kwargs)>1:
                #     obj = self.learner(self.kwargs['leaf_size'],self.verbose)
                # elif len(self.kwargs) ==1:
                #     obj = self.learner(self.verbose)
                # else:
                #     obj = self.learner(**self.kwargs)
                obj.add_evidence(sub_x, sub_y)
                instance_list.append(obj)
            return instance_list


        if self.verbose == True:
            try:
                self.instance_list = build_instance(data_x, data_y)
            except Exception as e:
                print(e)
        else:
            self.instance_list = build_instance(data_x, data_y)

    def query(self, points):
        """
        Estimate a set of test points given the model we built.

        :param points: A numpy array with each row corresponding to a specific query.
        :type points: numpy.ndarray
        :return: The predicted result of the input data according to the trained model
        :rtype: numpy.ndarray
        """

        def pred_value(points):
            y = []
            for ii in range(0, self.bags):
                pred_y = self.instance_list[ii].query(points)
                # if all(isinstance(e, (int, float)) for e in pred_y) == True:
                y.append(pred_y)
            ## calculate value one by one

            df = pd.DataFrame(data=y)
            results = []
            for series in df:
                results.append((df[series].drop_duplicates()).mean())
            return results



        if self.verbose == True:
            try:
                return pred_value(points)
            except Exception as e:
                print(e)
        else:
            return pred_value(points)

    

if __name__ == "__main__":
    alldata = np.genfromtxt('/Users/hy/Documents/ML4T_2023Fall/assess_learners/Data/simple.csv', delimiter=",")

    alldata = alldata[1:, 1:]
    train_x = alldata[:,:-1]
    train_y = alldata[:,-1]
    # learner = None, kwargs = None, bags = 1, boost = False, verbose = False
    start_time = time.time()

    obj = BagLearner(learner=rt.RTLearner, kwargs={"leaf_size":10}, bags=1, boost=False, verbose=False)
    # obj = BagLearner(learner=dt.DTLearner, kwargs={"leaf_size":1}, bags=1, boost=False, verbose=False)
    # obj = BagLearner(learner=lrl.LinRegLearner, kwargs={}, bags=1, boost=False, verbose=False)
    # obj = BagLearner(learner=it.InsaneLearner, kwargs={}, bags=1, boost=False, verbose=False)
    # obj = bl.BagLearner(learner=bl.BagLearner,
    #                      kwargs={'learner': lrl.LinRegLearner, 'kwargs': {}, 'bags': 20, 'boost': False,
    #                              'verbose': False},
    #                      bags=20, boost=False, verbose=False)
    obj.add_evidence(train_x, train_y)
    #     #
    #     #
    test_x = alldata[:, :-1]
    re = obj.query(test_x)
    # print("--- %s seconds ---" % (time.time() - start_time))

    # print(re)
    
    # obj = BagLearner(learner=rt.InsaneLearner, kwargs={"leaf_size":1, "verbose":False}, bags=1, boost=False, verbose=False)
    # obj = BagLearner(learner=lrl.LinRegLearner, kwargs={}, bags=1, boost=False, verbose=False)
    # obj = bl.BagLearner(learner=bl.BagLearner,
    #                     kwargs={'learner': lrl.LinRegLearner, 'kwargs': {}, 'bags': 20, 'boost': False,
    #                             'verbose': False},
    #                     bags=20, boost=False, verbose=False)
    # obj = bl.BagLearner(learner=it.InsaneLearner,
    #                     kwargs={'verbose': False},
    #                     bags=20, boost=False, verbose=False)
    
    # obj = BagLearner(learner=lrl.LinRegLearner, kwargs={}, bags=1, boost=False, verbose=False)
    # obj = bl.BagLearner(learner=bl.BagLearner,
    #                     kwargs={'learner':bl.BagLearner,
    #                           'kwargs': {'learner':rt.RTLearner,'kwargs':{'leaf_size':1, 'verbose': False}, 'bags':1, 'boost':False, 'verbose':False},
    #                               'bags':1, 'boos':False, 'verbose':False},
    #                               bags=10, boost=False, verbose=False)
                                 
    #
    #
    # obj.add_evidence(train_x, train_y)
    #
    #
    # test_x = alldata[:, :-1]
    # re = obj.query(test_x)
    # print(re)
    # #
    # test_x = alldata[:, :-1]

    # obj.add_evidence(train_x, train_y)

    # re = obj.query(test_x)

    # #
    #
    #
    #
    #
    # print(obj.instance_list[0].tree)

    # # print(obj.author())
    # test_x = alldata[101:105,:-1]
    # # #
    # #
    # y = obj.query(test_x)




    # obj = rt.RTLearner(1,True)
    # obj.add_evidence(train_x, train_y)
    # points = alldata[10:60,:-1]
    # print(obj.query(points))

