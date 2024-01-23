""" 			  		 			     			  	   		   	  			  	
MLP Model.  (c) 2021 Georgia Tech

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
np.random.seed(1024)
from ._base_network import _baseNetwork


class TwoLayerNet(_baseNetwork):
    def __init__(self, input_size=28 * 28, num_classes=10, hidden_size=128):
        super().__init__(input_size, num_classes)

        self.hidden_size = hidden_size
        self._weight_init()

    def _weight_init(self):
        """
        initialize weights of the network
        :return: None; self.weights is filled based on method
        - W1: The weight matrix of the first layer of shape (num_features, hidden_size)
        - b1: The bias term of the first layer of shape (hidden_size,)
        - W2: The weight matrix of the second layer of shape (hidden_size, num_classes)
        - b2: The bias term of the second layer of shape (num_classes,)
        """

        # initialize weights
        self.weights['b1'] = np.zeros(self.hidden_size)
        self.weights['b2'] = np.zeros(self.num_classes)
        np.random.seed(1024)
        self.weights['W1'] = 0.001 * np.random.randn(self.input_size, self.hidden_size)
        np.random.seed(1024)
        self.weights['W2'] = 0.001 * np.random.randn(self.hidden_size, self.num_classes)

        # initialize gradients to zeros
        self.gradients['W1'] = np.zeros((self.input_size, self.hidden_size))
        self.gradients['b1'] = np.zeros(self.hidden_size)
        self.gradients['W2'] = np.zeros((self.hidden_size, self.num_classes))
        self.gradients['b2'] = np.zeros(self.num_classes)

    def forward(self, X, y, mode='train'):
        """
        The forward pass of the two-layer net. 
        The activation function used in between the two layers is sigmoid, which
        is to be implemented in self.,sigmoid.
        The method forward should compute the loss of input batch X and gradients of each weights.
        Further, it should also compute the accuracy of given batch. The loss and
        accuracy are returned by the method and gradients are stored in self.gradients

        :param X: a batch of images (N, input_size)
        :param y: labels of images in the batch (N,)
        :param mode: if mode is training, compute and update gradients;else, just return the loss and accuracy
        :return:
            loss: the loss associated with the batch
            accuracy: the accuracy of the batch
            self.gradients: gradients are not explicitly returned but rather updated in the class member self.gradients
        """
        loss = None
        accuracy = None
        #############################################################################
        # TODO:                                                                     #
        #    1) Implement the forward process:                                      #
        #        1) Call sigmoid function between the two layers for non-linearity  #
        #        2) The output of the second layer should be passed to softmax      #
        #        function before computing the cross entropy loss                   #
        #    2) Compute Cross-Entropy Loss and batch accuracy based on network      #
        #       outputs                                                             #
        #############################################################################
        # z1i = sum(w1i*xi+b1i) 
        # 
        # active function： L1i_score = sigmoid(z1i)
        ## z2 = sum(w2i*L1i_score +b2i) 
        ## prob = softmax(z2)
        
        
        ## First Layer z is 64*128
        z1 = X.dot(self.weights['W1']) + self.weights['b1'] 
        ## sigmoid function between the two layers: L1_score 64*128
        L1_score = _baseNetwork(self.input_size,self.hidden_size).sigmoid(z1)
        
        ## Second Layer z is 64*10
        z2 = L1_score.dot(self.weights['W2']) + self.weights['b2'] 
        
        ## Compute the softmax probabilities 64
        prob = _baseNetwork(self.input_size,self.num_classes).softmax(z2)
        ## Compute the  Cross-Entropy loss
        loss = _baseNetwork(self.input_size,self.num_classes).cross_entropy_loss(prob, y)
        ## Compute the  accuracy
        accuracy = _baseNetwork(self.input_size,self.num_classes).compute_accuracy(prob, y)




        if mode != 'train':
            return loss, accuracy


        #############################################################################
        # TODO:                                                                     #
        #    1) Implement the backward process:                                     #
        #        1) Compute gradients of each weight and bias by chain rule         #
        #        2) Store the gradients in self.gradients                           #
        #    HINT: You will need to compute gradients backwards, i.e, compute       #
        #          gradients of W2 and b2 first, then compute it for W1 and b1      #
        #          You may also want to implement the analytical derivative of      #
        #          the sigmoid function in self.sigmoid_dev first                   #
        #############################################################################

        #############################################################################
        #                              END OF YOUR CODE                             #
        #############################################################################
        
        ## Compute gradients of each weight by chain rule   
        ## dw2 = L/S*S/A*A/w2
        ## L/S * S/A: For the true class in each sample,Sk is the predicted probability, 
        ## and Yi is 1. So, the gradient becomes Si -1 
        ## For all other classes Yj is 0, the gradient is Sj
        
        ## create Y_hat for the calcluation 
        Y_hat = np.zeros((prob.shape[0], self.num_classes))
        for ii in range(prob.shape[0]):
            Y_hat[ii,int(y[ii])] = 1         
        
        ## L/S * S/A: (prob -Y)/N 64*10
        dZ2 = (prob - Y_hat)/len(y)
        ## A/w2 = L1_score
        dW2 = L1_score.T.dot(dZ2)
        self.gradients['W2'] = dW2
        
        ## db2 = L/S*S/A*A/b2
        ## L/S * S/A: (prob -Y)/N which is dZ2 shown above
        ## A/b2 = 1  db2 is 10*1
        db2 =np.sum(dZ2.T,axis = 1)
        self.gradients['b2'] = db2
        
        ## dw1 = L/S*S/A*A/L1i_score*L1i_score/z1*z1/w1 
        ## A/L1i_score is w2: 128*10
        dL_L1 = dZ2.dot(self.weights['W2'].T)
        
        ## dL1i_score/z1 : 64*10
        dL1Z1 = _baseNetwork(self.input_size,self.num_classes).sigmoid_dev(z1)
        ## z1/b1 =>1   
       
        dW1 = X.T.dot(dL_L1*dL1Z1)
        self.gradients['W1'] = dW1
        
        ## db1 = L/S*S/A*A/L1i_score*L1i_score/z1*z1/b1
        
        db1 = np.sum(dL_L1*dL1Z1,axis = 0)
        self.gradients['b1'] = db1
        
        
        return loss, accuracy
if __name__ == "__main__":
    
    
    
        obj = TwoLayerNet()
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, os.pardir, 'tests/')
        test_batch = np.load(file_path+'softmax_grad_check/test_batch.npy')
        test_label = np.load(file_path+'softmax_grad_check/test_label.npy')
        
        
        
        model = TwoLayerNet(hidden_size=128)
        expected_loss = 2.30285
        w1_grad_expected = np.load(file_path+'twolayer_grad_check/w1.npy')
        b1_grad_expected = np.load(file_path+'twolayer_grad_check/b1.npy')
        w2_grad_expected = np.load(file_path+'twolayer_grad_check/w2.npy')
        b2_grad_expected = np.load(file_path+'twolayer_grad_check/b2.npy')

        loss, accuracy  = obj.forward(test_batch, test_label, mode='train')
        print('loss', loss - expected_loss)
        
        print('W2', np.sum(np.abs(w2_grad_expected - obj.gradients['W2'])))
        print('b2', np.sum(np.abs(b2_grad_expected - obj.gradients['b2'])))

        print('W1', np.sum(np.abs(w1_grad_expected - obj.gradients['W1'])))

        print('b1', np.sum(np.abs(b1_grad_expected - obj.gradients['b1'])))
