import BagLearner as bl
import LinRegLearner as lrl
import numpy as np
import InsaneLearner as it
class InsaneLearner(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
    def author(self):
        return "yhe600"  # replace tb34 with your Georgia Tech username
    def add_evidence(self, data_x, data_y):
        obj = bl.BagLearner(learner=bl.BagLearner,
                            kwargs={'learner':lrl.LinRegLearner,'kwargs':{},'bags':20, 'boost':False, 'verbose':self.verbose},
                           bags = 20, boost = False, verbose= False)
        ## call baglearner function
        obj.add_evidence(data_x, data_y)
        self.obj = obj
    def query(self, points):
       return self.obj.query(points)


