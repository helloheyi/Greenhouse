""" 			  		 			     			  	   		   	  			  	
Softmax Regression Model.  (c) 2021 Georgia Tech

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
import os
from ._base_network import _baseNetwork


class SoftmaxRegression(_baseNetwork):
    def __init__(self, input_size=28 * 28, num_classes=10):
        """
        A single layer softmax regression. The network is composed by:
        a linear layer without bias => (activation) => Softmax
        :param input_size: the input dimension
        :param num_classes: the number of classes in total
        """
        super().__init__(input_size, num_classes)
        self._weight_init()

    def _weight_init(self):
        '''
        initialize weights of the single layer regression network. No bias term included.
        :return: None; self.weights is filled based on method
        - W1: The weight matrix of the linear layer of shape (num_features, hidden_size)
        '''
        np.random.seed(1024)
        self.weights['W1'] = 0.001 * np.random.randn(self.input_size, self.num_classes)
        self.gradients['W1'] = np.zeros((self.input_size, self.num_classes))

    def forward(self, X, y, mode='train'):
        """
        Compute loss and gradients using softmax with vectorization.

        :param X: a batch of image (N, 28x28)
        :param y: labels of images in the batch (N,)
        :return:
            loss: the loss associated with the batch
            accuracy: the accuracy of the batch
        """
        loss = None
        gradient = None
        accuracy = None
        #############################################################################
        # TODO:                                                                     #
        #    1) Implement the forward process and compute the Cross-Entropy loss    #
        #    2) Compute the gradient of the loss with respect to the weights        #
        # Hint:                                                                     #
        #   Store your intermediate outputs before ReLU for backwards               #
        #############################################################################
        ## calcualte the fully-connected output.
        z = X.dot(self.weights['W1'])
        #############################################################################
        ## could score all zeros? 
        #############################################################################
        
        ## Use the ReLU activation function
        score = _baseNetwork(self.input_size,self.num_classes).ReLU(z)
        ## Compute the softmax probabilities
        prob = _baseNetwork(self.input_size,self.num_classes).softmax(score)
        ## Compute the  Cross-Entropy loss
        loss = _baseNetwork(self.input_size,self.num_classes).cross_entropy_loss(prob, y)
        ## Compute the  accuracy
        accuracy = _baseNetwork(self.input_size,self.num_classes).compute_accuracy(prob, y)
        
        if mode != 'train':
            return loss, accuracy

        #############################################################################
        # TODO:                                                                     #
        #    1) Implement the backward process:                                     #
        #        1) Compute gradients of each weight by chain rule                  #
        #        2) Store the gradients in self.gradients                           #
        #############################################################################

        ## Compute gradients of each weight by chain rule   
        ## L/S * S/A * A/Z *Z/W
       
        ## L/S * S/A: For the true class in each sample,Sk is the predicted probability, 
        ## and Yi is 1. So, the gradient becomes Si -1
        ## For all other classes Yj is 0, the gradient is Sj
        
        ## create Y_hat for the calcluation 
        Y_hat = np.zeros((prob.shape[0], self.num_classes))
        for ii in range(prob.shape[0]):
            Y_hat[ii,int(y[ii])] = 1 
        
        ## L/S * S/A: (prob -Y)/N
        dS_dA  = (prob-Y_hat)/len(y)
        
        # derviative of A respect to ReLU
        drelu = _baseNetwork(self.input_size,self.num_classes).ReLU_dev(z)
    
        # derviative of wi respect to Zi
        dZ = X
        ## apply chain rule 
        dW = (X.T).dot(dS_dA*drelu) 
        self.gradients['W1'] = dW
        return loss, accuracy

if __name__ == "__main__":
        obj = SoftmaxRegression()
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, os.pardir, 'tests/softmax_grad_check/')
        test_batch = np.load(file_path+'test_batch.npy')
        test_label = np.load(file_path+'test_label.npy')
        obj._weight_init()
        weights = obj.gradients
        loss, accuracy =  obj.forward(test_batch, test_label, mode='train')

        
        # z = np.array([[-1.48839468, -0.31530738],
        #       [-0.28271176, -1.00780433],
        #       [0.66435418, 1.2537461],
        #       [-1.64829182, 0.90223236]])
        
        # _baseNetwork(784,10).softmax(z)
        expected_grad = np.load(file_path+'softmax_relu_grad.npy')
        diff = np.sum(np.abs(expected_grad - obj.gradients['W1']))
        print(diff)
        