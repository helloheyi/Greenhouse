""" 			  		 			     			  	   		   	  			  	
Optimizer base.  (c) 2021 Georgia Tech

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
from models.softmax_regression import SoftmaxRegression
from models.two_layer_nn import TwoLayerNet

import numpy as np

class _BaseOptimizer:
    def __init__(self, learning_rate=1e-4, reg=1e-3):
        self.learning_rate = learning_rate
        self.reg = reg

    def update(self, model):
        pass

    def apply_regularization(self, model):
        """
        Apply L2 penalty to the model. Update the gradient dictionary in the model
        :param model: The model with gradients (Softmax - Regression)
        :return: None, but the gradient dictionary of the model should be updated
        """

        #############################################################################
        # TODO:                                                                     #
        #    1) Apply L2 penalty to model weights based on the regularization       #
        #       coefficient                                                         #
        
        model.gradients['W1'] = model.gradients['W1'] +self.reg* model.weights['W1']
        
        ## two layer 
        if len( model.gradients) > 1:
            model.gradients['W2'] = model.gradients['W2'] +self.reg* model.weights['W2']


if __name__ == "__main__":
    obj = _BaseOptimizer()
    model = SoftmaxRegression()
    
    w_grad = model.gradients['W1'].copy()
    obj.apply_regularization(model)
    w_grad_reg = model.gradients['W1']
    reg_diff = w_grad_reg - w_grad
    expected_diff = model.weights['W1'] * obj.reg

    diff = np.mean(np.abs(reg_diff - expected_diff))
    
    print(diff)
    
    

    model1 = TwoLayerNet()
    print(len(model1.gradients))
