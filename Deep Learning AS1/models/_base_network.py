""" 			  		 			     			  	   		   	  			  	
Models Base.  (c) 2021 Georgia Tech

Copyright 2021, Georgia Institute of Technology (Georgia Tech)
Atlanta, Georgia 30332
All Rights Reserved

Template code for CS 7643 Deep Learning

Georgia Tech asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including repositories
such as Github, Bitbucket, and Gitlab.  This copyright statement should
not be removed or edited.

Sharing solutions with current or future students of CS 7643 Deep Learning is
prohibited and subject to being investigated as a GT honor code violation.

-----do not edit anything above this line---
"""

# Do not use packages that are not in standard distribution of python
import numpy as np


class _baseNetwork:
    def __init__(self, input_size=28 * 28, num_classes=10):
        self.input_size = input_size
        self.num_classes = num_classes

        self.weights = dict()
        self.gradients = dict()

    def _weight_init(self):
        pass

    def forward(self):
        pass

    def softmax(self, scores):
        """
        Compute softmax scores given the raw output from the model

        :param scores: raw scores from the model (N, num_classes)
        :return:
            prob: softmax probabilities (N, num_classes)
        """
        prob = None
        #############################################################################
        # TODO:                                                                     #
        #    1) Calculate softmax scores of input images       
                     #
        ##(4,2),(4) => (4,2)
        prob =  np.exp(scores)/np.sum(np.exp(scores),axis=1, keepdims=True)
        return prob

    def cross_entropy_loss(self, x_pred, y):
        """
        Compute Cross-Entropy Loss based on prediction of the network and labels
        :param x_pred: Probabilities from the model (N, num_classes)
        :param y: Labels of instances in the batch
        :return: The computed Cross-Entropy Loss
        """
        #############################################################################
        # TODO:                                                                     #
        #    1) Implement Cross-Entropy Loss                                        #
        #############################################################################
        
        ## we need to determine the true label 
        
        loss = np.mean([-np.log(x_pred[ii,int(y[ii])]) for ii in range(0,len(y))])
        

        return loss

    def compute_accuracy(self, x_pred, y):
        """
        Compute the accuracy of current batch
        :param x_pred: Probabilities from the model (N, num_classes)
        :param y: Labels of instances in the batch
        :return: The accuracy of the batch
        """
        acc = None
        #############################################################################
        # TODO:                                                                     #
        #    1) Implement the accuracy function                                     #
        #############################################################################
        ## number of coorect predictions/ total number of predication 
        y_pred= np.argmax(x_pred,axis = 1) 
        acc = np.sum([1 for ii in range(0,len(y)) if y_pred[ii] ==y[ii]])/len(y)
        return acc

    def sigmoid(self, X):
        """
        Compute the sigmoid activation for the input

        :param X: the input data coming out from one layer of the model (N, layer size)
        :return:
            out: the value after the sigmoid activation is applied to the input (N, layer size)
        """
        #############################################################################
        # TODO: Comput the sigmoid activation on the input                          #
        #############################################################################
        out = np.zeros((np.shape(X)[0], np.shape(X)[1]))
        
        ## loop layer 
        for ii in range(0,np.shape(X)[1]):
            out[:,ii] = 1/ (1 + np.exp(-X[:,ii]))
        return out

    def sigmoid_dev(self, x):
        """
        The analytical derivative of sigmoid function at x
        :param x: Input data
        :return: The derivative of sigmoid function at x
        """
        #############################################################################
        # TODO:                                                                     #
        #    1) Implement the derivative of Sigmoid function                        #
        #############################################################################
        
        ds = self.sigmoid(x)*(1-self.sigmoid(x))
        

        return ds

    def ReLU(self, X):
        """
        Compute the ReLU activation for the input

        :param X: the input data coming out from one layer of the model (N, layer size)
        :return:
            out: the value after the ReLU activation is applied to the input (N, layer size)
        """
        #############################################################################
        # TODO: Comput the ReLU activation on the input                          #
        #############################################################################
        out = np.zeros((np.shape(X)[0], np.shape(X)[1]))

        ## loop layer 
        for ii in range(0,np.shape(X)[1]):
            out[:,ii] = [ X[jj,ii] if X[jj,ii] >0 else 0 for jj in range(0,len(X[:,ii]))]

        return out

    def ReLU_dev(self, X):
        """
        Compute the gradient ReLU activation for the input

        :param X: the input data coming out from one layer of the model (N, layer size)
        :return:
            out: gradient of ReLU given input X
        """
        out = np.zeros((np.shape(X)[0], np.shape(X)[1]))
        
        #############################################################################
        # TODO: Comput the gradient of ReLU activation                              #
        #############################################################################

        for ii in range(0,np.shape(X)[1]):
            out[:,ii] = [ 1 if X[jj,ii] >0 else 0 for jj in range(0,len(X[:,ii]))]

        return out

if __name__ == "__main__":
        obj = _baseNetwork()
        # x = np.array([[-1.48839468, -0.31530738],
        #               [-0.28271176, -1.00780433],
        #               [0.66435418, 1.2537461],
        #               [-1.64829182, 0.90223236]])
        # y = np.array([[0.0, 0.0],
        #               [0.0, 0.0],
        #               [0.66435418, 1.2537461],
        #               [0.0, 0.90223236]])
        # out = obj.ReLU(x)
        # diff = np.sum(np.abs((y - out)))
        # print(diff)
        
        
        # x = np.array([[-1.48839468, -0.31530738],
        #       [-0.28271176, -1.00780433],
        #       [0.66435418, 1.2537461],
        #       [-1.64829182, 0.90223236]])
        # y = np.array([[0.0, 0.0],
        #       [0.0, 0.0],
        #       [1., 1.],
        #       [0.0, 1.]])
        # out = obj.ReLU_dev(x)
        # diff = np.sum(np.abs((y - out)))
        # print(diff)
        
        
        x = np.array([[0.2, 0.5, 0.3], [0.5, 0.1, 0.4], [0.3, 0.3, 0.4]])
        y = np.array([1, 2, 0])
        expected_loss = 0.937803
        loss = obj.cross_entropy_loss(x, y)
        print(loss- expected_loss)
        # expected_acc = 0.3333

        
        # # acc = obj.compute_accuracy(x, y)
        # # print(acc- expected_acc)
        
        
        
        # # x = np.array([[-1.48839468, -0.31530738],
        # #       [-0.28271176, -1.00780433],
        # #       [0.66435418, 1.2537461],
        # #       [-1.64829182, 0.90223236]])
        # # y = np.array([[0.23629739, 0.76370261],
        # #       [0.67372745, 0.32627255],
        # #       [0.35677439, 0.64322561],
        # #       [0.07239128, 0.92760872]])
        # x = np.array([[-1, -2],
        #       [-3, -4],
        #       [-2,-1],
        #       [2, 1]])
        
        # out = obj.softmax(x)

        # print(np.sum(np.abs((y - out))))
        