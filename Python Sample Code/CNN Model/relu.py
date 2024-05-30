
import numpy as np


class ReLU:
    """
    An implementation of rectified linear units(ReLU)
    """

    def __init__(self):
        self.cache = None
        self.dx = None

    def forward(self, x):
        '''
        The forward pass of ReLU. Save necessary variables for backward
        :param x: input data
        :return: output of the ReLU function
        '''
        out = np.maximum(0,x)

        #############################################################################
        # TODO: Implement the ReLU forward pass.                                    #
        #############################################################################

        self.cache = x
        return out
    
    def backward(self, dout):
        """
        :param dout: the upstream gradients
        :return:
        """
        #############################################################################
        # TODO: Implement the ReLU backward pass.                                   #
        #############################################################################
        dx, x = None, self.cache
        
        out = np.where(x <= 0, 0, 1) 
        
        dx = dout*out
        self.dx = dx
if __name__ == "__main__":
    relu = ReLU()
    x_shape = (2, 2, 2, 2)
    x = np.linspace(-0.1, 0.5, num=np.prod(x_shape)).reshape(x_shape)


    # correct_out = np.array([[0., 0., 0., 0., ],
    #                            [0., 0., 0.04545455, 0.13636364, ],
    #                            [0.22727273, 0.31818182, 0.40909091, 0.5, ]])
    # print(correct_out-out)
    
    
