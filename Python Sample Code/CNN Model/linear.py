

import numpy as np


class Linear:
    """
    A linear layer with weight W and bias b. Output is computed by y = Wx + b
    """

    def __init__(self, in_dim, out_dim):
        self.in_dim = in_dim
        self.out_dim = out_dim

        self.cache = None

        self._init_weights()

    def _init_weights(self):
        np.random.seed(1024)
        self.weight = 1e-3 * np.random.randn(self.in_dim, self.out_dim)
        np.random.seed(1024)
        self.bias = np.zeros(self.out_dim)

        self.dx = None
        self.dw = None
        self.db = None

    def forward(self, x):
        """
        Forward pass of linear layer
        :param x: input data, (N, d1, d2, ..., dn) where the product of d1, d2, ..., dn is equal to self.in_dim
        :return: The output computed by Wx+b. Save necessary variables in cache for backward
        """
        out = None
        #############################################################################
        # TODO: Implement the forward pass.                                         #
        #    HINT: You may want to flatten the input first                          #
        #############################################################################
        ## w is 120*3; b is (3,); 
        ##x is (2,4,5,6) -> 2*120 
        ## (each of the 2 elements in the first dimension will be associated with a flattened array of 120 elements )
        
        
        
        x_reshape =  x.reshape(np.shape(x)[0], np.shape(self.weight)[0])
        out = x_reshape.dot(self.weight) + self.bias
        
        ## don't save reshape one 
        self.cache = x
        return out

    def backward(self, dout):
        """
        Computes the backward pass of linear layer
        :param dout: Upstream gradients, (N, self.out_dim)
        :return: nothing but dx, dw, and db of self should be updated
        """
        x = self.cache
        ## dout (10,5)
       
        ## dout/db = 1  
        db = np.sum(dout.T,axis = 1)
        self.db = db
        
        ## dout/dw  = x x: 10*6, dout: (10,5) 
        ## dw =>6*5
        ## need to reshape x 
        x_reshape = x.reshape(np.shape(x)[0], np.shape(self.weight)[0])
        dw = x_reshape.T.dot(dout)
        self.dw = dw
        
        ## dout/dx  = w: 6*5, dout: (10,5) 
        ## dx => 10*6
        dx = dout.dot(self.weight.T)
        
        ## make it same as x shape
        dx = dx.reshape(x.shape)
        self.dx = dx
        
        
        

       
if __name__ == "__main__":

    x = np.random.randn(4, 32,50,50)

    # dx_num = eval_numerical_gradient_array(lambda x:layer.forward(x), x, dout)
    
    # backward(self, dout)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
