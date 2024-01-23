""" 			  		 			     			  	   		   	  			  	
SGD Optimizer.  (c) 2021 Georgia Tech

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

## need change back ..... 
# from optimizer._base_optimizer import _BaseOptimizer
# import numpy as np
# from models.softmax_regression import SoftmaxRegression
# from models.two_layer_nn import TwoLayerNet
# import os
from ._base_optimizer import _BaseOptimizer

class SGD(_BaseOptimizer):
    def __init__(self, learning_rate=1e-4, reg=1e-3):
        super().__init__(learning_rate, reg)

    def update(self, model):
        """
        Update model weights based on gradients
        :param model: The model to be updated
        :return: None, but the model weights should be updated
        """
        self.apply_regularization(model)
        #############################################################################
        # TODO:                                                                     #
        #    1) Update model weights based on the learning rate and gradients       #
        #############################################################################

        model.weights['W1'] = model.weights['W1'] - self.learning_rate * model.gradients['W1']
        
        ## two layer 
        if len( model.gradients) > 1:
            model.weights['W2'] = model.weights['W2'] - self.learning_rate * model.gradients['W2']

        #############################################################################
        #                              END OF YOUR CODE                             #
        #############################################################################


# if __name__ == "__main__":
#     obj = SGD(learning_rate=1e-3, reg=1e-3)
#     model = SoftmaxRegression()
    
#     np.random.seed(256)
#     fake_gradients = np.random.randn(784, 10)
#     model.gradients['W1'] = fake_gradients
#     obj.update(model)
#     current_dir = os.getcwd()
#     file_path = os.path.join(current_dir, os.pardir, 'tests/')
#     expected_weights = np.load(file_path + 'sgd/sgd_updated_weights.npy')
#     diff = np.abs(expected_weights - model.weights['W1'])
#     diff = np.sum(diff)
    