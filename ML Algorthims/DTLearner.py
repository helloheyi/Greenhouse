""""""
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
import warnings
warnings.filterwarnings("ignore")


class DTLearner(object):
    """
    This is a Decision Tree Learner. It is implemented correctly.

    :param verbose: If “verbose” is True, your code can print out information for debugging.
        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.
    :type verbose: bool
    """

    def __init__(self, leaf_size, verbose):
        """
        Constructor method
        """
        ## leaf_size hyperparamter
        self.leaf_size = leaf_size
        ## debug parameter
        self.verbose = verbose

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
        def build_tree_(data_x, data_y):

            if len(data_y) <= self.leaf_size and len(data_y) > 0:
                # Return leaf val by take mean of sample
                leaf_val = np.mean(data_y)
                return np.array([True, np.nan, np.nan, leaf_val], dtype=object)

            if len(np.unique(data_y)) == 1:
                # Return leaf val by take mean of sample
                leaf_val = np.mean(data_y)
                return np.array([True, np.nan, np.nan, leaf_val], dtype=object)

            else:
                node = 0
                corr = 0
                corrr_list = np.array([],dtype=float)
                index_list = np.array([],dtype=int)
                ## determine best feature ii to split
                for ii in range(np.shape(data_x)[1]):
                    # Calculate the correlation between the feature and labels
                    temp = np.correlate(data_x[:, ii], data_y)[0]
                    if temp>1 or temp<-1:
                        temp = 0

                    if abs(temp) > abs(corr):
                         corr = temp
                         node = ii
                    index_list = np.append(index_list,ii)
                    corrr_list = np.append(corrr_list,abs(temp))


                inform = np.array([corrr_list,index_list], dtype=object)
                sorted_val = np.argsort(inform[0])[::-1]
                inform = inform[:, sorted_val]
                jj = 0
                ## calculate split value
                splitval = np.median(data_x[:, node])
                # build left and right tree
                left_indices = np.where(data_x[:, node] <= splitval)[0]
                right_indices = np.where(data_x[:, node] > splitval)[0]
                # check empty subtree then regenerate splitval to split tree
                ## make sure out of loop
                ## check indices is zero or not.
                while (len(right_indices) == 0 or len(left_indices) == 0) and max(len(left_indices),len(right_indices)) > self.leaf_size and jj <(np.shape(data_x)[1]-1):
                    jj=jj+1
                    node = inform[1,jj]
                    splitval = np.median(data_x[:, node])
                    left_indices = np.where(data_x[:, node] <= splitval)[0]
                    right_indices = np.where(data_x[:, node] > splitval)[0]

                if (len(right_indices) == 0 or len(left_indices) == 0) and max(len(left_indices),len(right_indices)) > self.leaf_size:
                # ## get unique data set (drop replicate row)
                    splitval = np.median(np.unique(data_x[left_indices], axis=0)[:, node])
                    left_indices = np.where(data_x[:, node] <= splitval)[0]
                    right_indices = np.where(data_x[:, node] > splitval)[0]

                left_tree = build_tree_(data_x[left_indices], data_y[left_indices])
                right_tree = build_tree_(data_x[right_indices], data_y[right_indices])
                root = np.array([False, node, splitval, left_tree, right_tree], dtype=object)
                # return np array
                return root

        if self.verbose == True:
            try:
                self.tree = build_tree_(data_x, data_y)
            except Exception as e:
                print(e)
        else:
            self.tree = build_tree_(data_x, data_y)

    def query(self, points):
        """
        Estimate a set of test points given the model we built.

        :param points: A numpy array with each row corresponding to a specific query.
        :type points: numpy.ndarray
        :return: The predicted result of the input data according to the trained model
        :rtype: numpy.ndarray
        """
        def pred_value(tree, x):
            if tree[0] == True:
                return tree[-1]
            else:

                if x[tree[1]] <= tree[2]:
                    tree = tree[3]
                    return pred_value(tree, x)
                else:
                    tree = tree[4]
                    return pred_value(tree, x)

        def loop_sample(points):
            y = np.array([],dtype=float)

            if len(np.shape(points)) ==1:
                y = np.append(y, pred_value(self.tree, points))
                return y
            else:
                for x in points:
                    y = np.append(y,pred_value(self.tree, x))
                return y

        if self.verbose == True:
            try:
                return loop_sample(points)
            except Exception as e:
                print(e)
        else:
            return loop_sample(points)



if __name__ == "__main__":
    # alldata = np.genfromtxt(os.path.join(os.path.dirname(__file__), 'Data/Book20.csv'), delimiter=",")
    # alldata = np.genfromtxt(os.path.join(os.path.dirname(__file__), 'test1.csv'), delimiter=",")
    alldata = np.genfromtxt(os.path.join(os.path.dirname(__file__), 'Data/Istanbul.csv'), delimiter=",")

    alldata = alldata[1:, 1:]
    train_x = alldata[:,:-1]
    train_y = alldata[:,-1]
    obj = DTLearner(1,False)
    obj.add_evidence(train_x, train_y)
    #
    test_x = alldata[:, :-1]
    # print(obj.query(test_x))