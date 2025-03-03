

import numpy as np


class Conv2D:
    '''
    An implementation of the convolutional layer. We convolve the input with out_channels different filters
    and each filter spans all channels in the input.
    '''

    def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, padding=0):
        """
        :param in_channels: the number of channels of the input data
        :param out_channels: the number of channels of the output(aka the number of filters applied in the layer)
        :param kernel_size: the specified size of the kernel(both height and width)
        :param stride: the stride of convolution
        :param padding: the size of padding. Pad zeros to the input with padding size.
        """
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding

        self.cache = None

        self._init_weights()

    def _init_weights(self):
        np.random.seed(1024)
        
        ## out_channels, in_channels, kernel_size, kernel_size
        
        self.weight = 1e-3 * np.random.randn(self.out_channels, self.in_channels, self.kernel_size, self.kernel_size)
        self.bias = np.zeros(self.out_channels)

        self.dx = None
        self.dw = None
        self.db = None

    def forward(self, x):
        """
        The forward pass of convolution
        :param x: input data of shape (N, C, H, W)
        :return: output data of shape (N, self.out_channels, H', W') where H' and W' are determined by the convolution
                 parameters. Save necessary variables in self.cache for backward pass
        """
        out = None
        #############################################################################
        # arr = [1, 3, 2, 5, 4] 
        # padding array using CONSTANT mode 
        # pad_arr = np.pad(arr, (3, 2), 'constant',  constant_values=(6, 4)) 
        # output: [6 6 6 1 3 2 5 4 4 4]
        #############################################################################
        ## output size 
        h_outdim = (np.shape(x)[2] - self.kernel_size + 2*self.padding)//self.stride +1
        w_outdim = (np.shape(x)[3] - self.kernel_size + 2*self.padding)//self.stride +1
        out = np.zeros((np.shape(x)[0],self.out_channels, h_outdim,w_outdim))
        
        ## add padd
        x_padded = np.pad(x, [(0, 0), (0, 0), (self.padding, self.padding), (self.padding, self.padding)], mode='constant')

        ### think about how to automatic these four loop 
        ## a good reference https://www.songho.ca/dsp/convolution/convolution2d_example.html

        ## n: in_channels
        for n in range(0,np.shape(x)[0]):
            ### c: out_channels
            for c in  range(0,np.shape(self.weight)[0]):
                for h in  range(0,h_outdim):
                    for w in  range(0,w_outdim):
                       
                        ## all out channels need to calculate  
                        ## move kneral window 
                        matrix = x_padded[n,:,h * self.stride:np.shape(self.weight)[2] + h * self.stride,w * self.stride:np.shape(self.weight)[3]+ w * self.stride]
                        out[n,c,h,w] = np.sum(matrix*self.weight[c, :, :, :]) + self.bias[c]
        self.cache = x
        return out

    def backward(self, dout):
        """
        The backward pass of convolution
        :param dout: upstream gradients
        :return: nothing but dx, dw, and db of self should be updated
        """
        x = self.cache
       
        ## dout/db = 1  => (out.channels)
        db = np.sum(dout, axis=(0,2,3))
        self.db = db
        
        ## dout/dw  = x w: [out_channels, in_channels, kernel_size, kernel_size]
        ## dw => (2, 3, 3, 3)
        ##  x => (4, 3, 5, 5);  dout => (4, 2, 5, 5)
        ##  first step add padding
        x_padded = np.pad(x, [(0, 0), (0, 0), (self.padding, self.padding), (self.padding, self.padding)], mode='constant', constant_values=0)
        dx_padded = np.zeros_like(x_padded)
        dw =  np.zeros_like(self.weight)
        c_dim,_,k_h,k_w = self.weight.shape
                   
        
        # llop batch 
        for n in range(x.shape[0]):
            ### c: out_channels -- check out channel
            for c in range(0, self.out_channels):
                for h in range(0, dout.shape[2]):
                    for w in range(0, dout.shape[3]):
                        
                        
                        h_start = h*self.stride
                        h_end = h*self.stride+k_h
                        w_start = w*self.stride
                        w_end = w*self.stride+k_w
                        ## based on TA's note the formula as following: dout/dw  = x 
                        dw[c,:,:,:] = dw[c,:,:,:] + x_padded[n,:,h_start:h_end,w_start:w_end]*dout[n,c,h,w]
                        
                        ## dout/dx  = w 
                        dx_padded[n,:,h_start:h_end,w_start:w_end] = dx_padded[n,:,h_start:h_end,w_start:w_end]+ self.weight[c,: , :, :] * dout[n, c,h,w]

        
        self.dw = dw
    # Reassigning dx by slicing dx_padded
    
        if self.padding > 0:
            self.dx = dx_padded[:, :, self.padding:-(self.padding), self.padding:-(self.padding)]
        else:
            self.dx = dx_padded




if __name__ == "__main__":
    # x_shape = (2, 3, 4, 4)
    # w_shape = (3, 3, 4, 4)
    # x = np.linspace(-0.1, 0.5, num=np.prod(x_shape)).reshape(x_shape)
    # w = np.linspace(-0.2, 0.3, num=np.prod(w_shape)).reshape(w_shape)
    # b = np.linspace(-0.1, 0.2, num=3)
    
    # correct_out = np.array([[[[-0.08759809, -0.10987781],
    #                               [-0.18387192, -0.2109216]],
    #                               [[0.21027089, 0.21661097],
    #                               [0.22847626, 0.23004637]],
    #                               [[0.50813986, 0.54309974],
    #                               [0.64082444, 0.67101435]]],
    #                             [[[-0.98053589, -1.03143541],
    #                               [-1.19128892, -1.24695841]],
    #                               [[0.69108355, 0.66880383],
    #                               [0.59480972, 0.56776003]],
    #                               [[2.36270298, 2.36904306],
    #                               [2.38090835, 2.38247847]]]])
    # obj = Conv2D(3, 3, 4, 2, 1)

    # obj.weight = w
    # obj.bias = b
    # out = obj.forward(x)
    
    x_shape = (4, 3, 5, 5)
    w_shape = (2, 3, 3, 3)
    dout_shape = (4, 2, 5, 5)
    x = np.linspace(-0.1, 0.5, num=np.prod(x_shape)).reshape(x_shape)
    w = np.linspace(-0.2, 0.3, num=np.prod(w_shape)).reshape(w_shape)
    dout = np.linspace(1, 1.5, num=np.prod(dout_shape)).reshape(dout_shape)
    b = np.linspace(-0.1, 0.2, num=2)
    obj = Conv2D(3, 2, 3, 1, 1)

    obj.weight = w
    obj.bias = b
    out = obj.forward(x)

    # w = np.array([[[[1, 0, -1],[1, 0, -1],[1, 0, -1]]]])
    # b = [0]
    # obj = Conv2D(1, 1, 3, 1, 0)
    # obj.weight = w
    # obj.bias = b
    # out = obj.forward(x)
    # print("Output shape:", out)

