#import perceptron2_package as perc

from sklearn import datasets
from sklearn.utils import shuffle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#perc.test_package()


wdbc = pd.read_csv("/Users/dominiquepaul/xJob/DataWithPythonCourse1/Data/wbdc.csv")
wdbc.replace(["M","B"],[0,1], inplace = True)

perc_train = 0.7

wdbc = shuffle(wdbc, random_state = 1).reset_index().drop(["index"],axis=1)
wdbc.head()

#split the set into training and test set
training_set_wdbc = wdbc.iloc[0:round(perc_train*len(wdbc)),:]
test_set_wdbc = wdbc.iloc[round(perc_train*len(wdbc)):,:]




class perceptron(object):
    """
    Parameters
    ------------
    eta : determines the learning rate, float value

    Attributes
    -----------
    w_ : weight array
    bookkeeping_ : data frame describing the development of the parameters during the learning
                    process
    weightsdf_ : data frame describing the development of the weights during the learning process.
                    Is later merged into bookkeeping_
    """

    def __init__(self,eta = 0.01):
        self.eta = eta


    def fit(self,training_set,y):
        # initialize weights as an array of the length of the amount of columns in
        # the training set plus one more for the w_0 weight
        self.w_ = np.zeros(training_set.shape[1]+1)
        # insert a manual counting variable which is used for indexing
        self.iteration = 1
        # initiate a data frame to keep a record on the development during each iteration
        self.bookkeeping_ = pd.DataFrame(index = np.arange(0,70,1), columns = ["iter", "misclas","false_positives","false_negatives"])
        self.weightsdf_ = pd.DataFrame(0,index = np.arange(0,70,1), columns = range(3))
        for features_i, target in zip(training_set, y):
            update = self.eta*(target - self.predict(features_i))
            self.w_[0] += update
            self.w_[1:] += update * features_i

            # do the bookkeeping_
            self.bookkeeping_.ix[self.iteration-1,"iter"] = self.iteration
            mistakes = sum(np.where(y == self.predict(training_set),0,1))/len(training_set)
            self.bookkeeping_.ix[self.iteration-1,"misclas"] = mistakes

            # false positives
            false_positives = sum(np.where((self.predict(training_set) == 1) & (y == -1) ,1,0))/ np.sum(np.array(y) == -1)
            self.bookkeeping_.ix[self.iteration-1,"false_positives"] = false_positives
            # false negatives
            false_negatives = sum(np.where((self.predict(training_set) == -1) & (y == 1),1,0))/ np.sum(np.array(y) == 1)
            self.bookkeeping_.ix[self.iteration-1,"false_negatives"] = false_negatives

            for i in np.arange(0,training_set.shape[1]+1,1):
                self.weightsdf_.ix[self.iteration-1,i] = self.w_[i]

            self.iteration += 1

        self.bookkeeping_ = self.bookkeeping_.join(self.weightsdf_)

    def predict(self, set):
        index = self.w_[0] + np.dot(set, self.w_[1:])
        prediction = np.where(index > 0, 1, -1)
        return prediction
        
        
x = perceptron(0.01)
x.fit(training_set_wdbc.iloc[:,3:33].values, training_set_wdbc.iloc[:,2].values)
     
x.weightsdf_
# apply to the testing set
evaluation = test_set_wdbc
evaluation["result"] = np.where(evaluation["diagnosis"] == x.predict(test_set_wdbc.iloc[:,3:33].values), "correct", "false")
evaluation   
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
