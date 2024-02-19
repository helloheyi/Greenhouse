

import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import datetime as dt

class RTLearner(object):
    """
    This is a random tree Learner. It is implemented correctly.

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
        self.verbose = verbose
          # move along, these aren't the drones you're looking for

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
        # Set the seed to a specific value, such as 42
        def build_tree_(data_x, data_y):
            if len(data_y) <= self.leaf_size and len(data_y) > 0:
                # Return leaf val by take mean of sample
                leaf_val = np.mean(data_y)
                # if leaf_val > 0.6:
                #     leaf_val = 1
                # elif leaf_val<-0.6:
                #     leaf_val = -1
                # else:
                #     leaf_val = 0
                return np.array([True, np.nan, np.nan, leaf_val], dtype=object)


            if len(np.unique(data_y)) == 1:
                # Return leaf val by take mean of sample
                leaf_val = np.mean(data_y)
                # if leaf_val > 0.5:
                #     leaf_val = 1
                # elif leaf_val<-0.5:
                #     leaf_val = -1
                # else:
                #     leaf_val = 0
                return np.array([True, np.nan, np.nan, leaf_val], dtype=object)
            else:
                node = 0
                corr = 0
                ## random to pick up node determine best feature ii to split
                ## the “half-open” interval [low, high)
                node = np.random.randint(0,np.shape(data_x)[1],dtype=int)
                ## random pick up two points under x_node
                ## make sure we have enough dataset
                if np.shape(data_x)[0] > 1:
                    index_list = np.array([],dtype=int)
                    while len(index_list) < 2:
                        random_Index = np.random.randint(0, np.shape(data_x)[0], dtype=int)
                        if random_Index not in index_list:
                            index_list = np.append(index_list,random_Index)

                    point1 = data_x[index_list[0], node]
                    point2 = data_x[index_list[1], node]
                    splitval = (point1 + point2) / 2

                else:
                    splitval = data_x[:, node]
                left_indices = np.where(data_x[:, node] <= splitval)[0]
                right_indices = np.where(data_x[:, node] > splitval)[0]

                # build left and right tree

                while (len(right_indices) == 0 or len(left_indices) == 0) and max(len(left_indices),len(right_indices)) > self.leaf_size:
                    node = np.random.randint(0, np.shape(data_x)[1], dtype=int)
                    index_list = np.array([],dtype=int)
                    while len(index_list) < 2:
                        random_Index = np.random.randint(0, np.shape(data_x)[0], dtype=int)
                        if random_Index not in index_list:
                            index_list = np.append(index_list,random_Index)

                    point1 = data_x[index_list[0], node]
                    point2 = data_x[index_list[1], node]
                    splitval = (point1 + point2) / 2
                    left_indices = np.where(data_x[:, node] <= splitval)[0]
                    right_indices = np.where(data_x[:, node] > splitval)[0]

                ## build empty tree constrain
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
            if x[tree[1]] <= tree[2]:
                tree = tree[3]
                return pred_value(tree, x)
            else:
                tree = tree[4]
                return pred_value(tree, x)


        def loop_sample(points):
            y = np.array([],dtype=float)

            if len(np.shape(points)) == 1:
                y = y.append(y, pred_value(self.tree, points))
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
    df = (pd.read_csv('Train.csv'))
    print(df)
    trainY = df.iloc[:, -1].values
    trainX = df.iloc[:, 1:-1].values
    obj = RTLearner(5, False)


    obj.add_evidence(trainX, trainY)
    obj_tree = obj.tree
    print(obj.tree)
    df_test = pd.read_csv('testX.csv',parse_dates=True)

    testX = np.array(df.iloc[:, 1:-1])
    val =obj.query(testX)
    print(val)
    # alldata = np.genfromtxt(os.path.join(os.path.dirname(__file__), 'Data/Istanbul.csv'), delimiter=",")
    # alldata = alldata[1:, 1:]
    # train_x = alldata[:,:-1]
    # train_y = alldata[:,-1]
    # test_x = alldata[:, :-1]
    # obj = RTLearner(1, False)
    #
    # root = obj.add_evidence(train_x, train_y)
    # val =obj.query(test_x)
    # print(val)



    # print(obj.add_evidence(train_x, train_y))
    # print(obj.query(points))



