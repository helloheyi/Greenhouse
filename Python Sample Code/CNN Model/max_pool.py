

import numpy as np


class MaxPooling:
    """
    Max Pooling of input
    """

    def __init__(self, kernel_size, stride):
        self.kernel_size = kernel_size
        self.stride = stride
        self.cache = None
        self.dx = None

    def forward(self, x):
        """
        Forward pass of max pooling
        :param x: input, (N, C, H, W)
        :return: The output by max pooling with kernel_size and stride
        """
        out = None
        #############################################################################
        # TODO: Implement the max pooling forward pass.                             #
        # Hint:                                                                     #
        #       1) You may implement the process with loops                         #
        #############################################################################

       
       ## out dimension is (N,C,(H-kernel_size)/stride+1,(W-kernel_size)/stride+1)
        H_dimout = (np.shape(x)[2] -  self.kernel_size)//self.stride +1
        W_dimout = (np.shape(x)[3] -  self.kernel_size)//self.stride +1
        
        out = np.zeros((np.shape(x)[0],np.shape(x)[1], H_dimout,W_dimout))
        ## get max index value 
        index_out = []
        ### think about how to automatic these four loop 
        for n in range(0,np.shape(x)[0]):
            for c in  range(0,np.shape(x)[1]):
                for h in  range(0,H_dimout):
                    for w in  range(0,W_dimout):
                        matrix = x[n,c,h * self.stride:self.kernel_size + h * self.stride,w * self.stride:self.kernel_size + w * self.stride]
                        out[n,c,h,w] = np.max(matrix)
                       
                        # np.unravel_index Convert the flat index to 2D coordinates
                        #    shape = (3, 4)
                            
                            # Example flat index
                         #   flat_index = 5
                            
                            # Convert the flat index to 2D coordinates
                          #  coords = np.unravel_index(flat_index, shape)
                        
                        ## save the max index and it will used on backward
                        
                        flat_index = np.argmax(matrix)
                        max_index = np.unravel_index(flat_index, matrix.shape)
                        index_out.append((n,c,max_index[0]+h * self.stride,  max_index[1]+w * self.stride ))
                        # Max Pooling of input         
       
        ## what is H_out, W_out    

        self.cache = (x, index_out)
        return out

    def backward(self, dout):
        """
        Backward pass of max pooling
        :param dout: Upstream derivatives
        :return: nothing, but self.dx should be updated
        """
        x, index_out = self.cache
        #############################################################################
        # TODO: Implement the max pooling backward pass.                            #
        # Hint:                                                                     #
        #       1) You may implement the process with loops                     #
        #       2) You may find np.unravel_index useful                             #
       
        #############################################################################
        

        ## df(max(x))/ x => max pooling is 1 at max value otherwise is 0
        ## dx is the same size as x so create a empty matrix 
        dx = np.zeros(x.shape)
        flat_dout = dout.reshape(len(index_out))
        for ii in range(0,len(index_out)):
            dx[index_out[ii]] = flat_dout[ii]
        self.dx = dx
       






if __name__ == "__main__":      
    
    x_shape = (2, 3, 4, 4)
    x = np.linspace(-0.3, 0.4, num=np.prod(x_shape)).reshape(x_shape)
    correct_out = np.array([[[[-0.26315789, -0.24842105],
                                  [-0.20421053, -0.18947368]],
                                 [[-0.14526316, -0.13052632],
                                  [-0.08631579, -0.07157895]],
                                 [[-0.02736842, -0.01263158],
                                  [0.03157895, 0.04631579]]],
                                [[[0.09052632, 0.10526316],
                                  [0.14947368, 0.16421053]],
                                 [[0.20842105, 0.22315789],
                                  [0.26736842, 0.28210526]],
                                 [[0.32631579, 0.34105263],
                                  [0.38526316, 0.4]]]])
    obj = MaxPooling(2,2)
    out = obj.forward(x)
    x_shape = (2, 3, 4, 4)
    x = np.linspace(-0.3, 0.4, num=np.prod(x_shape)).reshape(x_shape)
    dout_shape = (2, 3, 2, 2)  # Example gradient from the next layer
    dout = np.linspace(-0.3, 0.4, num=np.prod(dout_shape)).reshape(dout_shape)
    obj.backward(dout)
    dx_test = obj.dx
