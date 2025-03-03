import numpy as np

class ConvNet:
    """
    Max Pooling of input
    """
    def __init__(self, modules, criterion):
        self.modules = []
        for m in modules:
            if m['type'] == 'Conv2D':
                self.modules.append(
                    Conv2D(m['in_channels'],
                           m['out_channels'],
                           m['kernel_size'],
                           m['stride'],
                           m['padding'])
                )
            elif m['type'] == 'ReLU':
                self.modules.append(
                    ReLU()
                )
            elif m['type'] == 'MaxPooling':
                self.modules.append(
                    MaxPooling(m['kernel_size'],
                               m['stride'])
                )
            elif m['type'] == 'Linear':
                self.modules.append(
                    Linear(m['in_dim'],
                           m['out_dim'])
                )
        if criterion['type'] == 'SoftmaxCrossEntropy':
            self.criterion = SoftmaxCrossEntropy()
        else:
            raise ValueError("Wrong Criterion Passed")

    def forward(self, x, y):
        """
        The forward pass of the model
        :param x: input data: (N, C, H, W)
        :param y: input label: (N, )
        :return:
          probs: the probabilities of all classes: (N, num_classes)
          loss: the cross entropy loss
        """
        probs = None
        loss = None
        for fun in self.modules: 
            x = fun.forward(x)
        
        ##  get dimension of linear weight   
        self.weight = fun.weight 
        self.bias = fun.bias     
        probs, loss = self.criterion.forward(x,y)
        return probs, loss

    
    def backward(self):
        """
        The backward pass of the model
        :return: nothing but dx, dw, and db of all modules are updated
        """
        ## loop for dx 
        self.criterion.backward()
        dx = self.criterion.dx
        for fun in self.modules[::-1]: 
            fun.backward(dx)
            dx = fun.dx

       
        self.dx = dx
        self.dw = fun.dw
        self.db = fun.db
        
        
# if __name__ == "__main__":
#     model_list = [dict(type='Relu')]
#     criterion = dict(type='SoftmaxCrossEntropy')
#     model = ConvNet(model_list, criterion)
#     for idx, m in enumerate(model.modules):
#         print('idx',idx)
#         print('m',m)

#     # forward once
#     np.random.seed(1024)
#     x = np.random.randn(32, 128)
#     np.random.seed(1024)
#     y = np.random.randint(10, size=32)
#     tmp = model.forward(x, y)
#     model.backward()
#     for idx, m in enumerate(model.modules):
#         print('idx',idx)
#         print('m',m)
    
    
    
#     df = pd.read_csv('/Users/hy/Desktop/DL/SP24/AS2/assignment2-spring2024/part1-convnet/data/mnist_test.csv')
    
#     y = df.iloc[0:4,-1].to_numpy()
#     x = np.random.randn(4, 3, 100, 100)

    
#     model_list = [dict(type='Conv2D', in_channels=3, out_channels=32, kernel_size=5, stride=1, padding=2),
#               dict(type='ReLU'),
#               dict(type='MaxPooling', kernel_size=2, stride=2),
#               dict(type='Linear', in_dim=80000, out_dim=10)]
#     # dict(type='Linear', in_dim=8192, out_dim=10)
#     criterion = dict(type='SoftmaxCrossEntropy')
    
#     model = ConvNet(model_list, criterion)
        
#     model.forward(x, y)
    
    
#     # model.backward()
#     model.criterion.backward()
#     dx = model.criterion.dx
    
   
#     # model.modules[-1].backward(dx)
    
    # dx = model.modules[-1].dx
    # print(np.shape(dx))
    
    
    
    
    
    
    
    
    
    # dx = model.criterion.dx
    
    # model.modules[-1].backward(dx)
    
    
    
    
    # model.criterion.backward(model.out,y) 


    
    
    
