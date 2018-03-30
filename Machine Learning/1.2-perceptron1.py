"""
perceptron 1.0:
this version of the code *OMITS* a bookkeeping file which tracks 
the development of model as it passes through several iterations
"""

from sklearn import datasets
from sklearn.utils import shuffle
import pandas as pd
import numpy as np

perc_train = 0.7 # the training set size as percentage of overall set

# Prepare data for use --------------------------------------------------------------

# load the data from sklearn
iris = datasets.load_iris()
data = pd.DataFrame(iris.data).iloc[:,[1,3]]
 
# add column with the classification labels
data = data.join(pd.DataFrame(iris.target))
# rename columns
data.columns = ["Sepal_length", "Petal_length","Target"]


# add new column for text labelling of flower
data.loc[:,"Type"] = data["Target"]
data.loc[:,"Type"].replace([0,1,2], ["Setosa","Versicolor","Virginica"], inplace = True)

# Delete all virginica rows
data1 = data.loc[data.loc[:,"Type"].isin(["Setosa","Versicolor"])]

# change target values in our data from 0/1 to -1/1
data1.loc[:,"Target"].replace([0],[-1], inplace=True)
data1

#shuffle data set
data2 = shuffle(data1, random_state = 1).reset_index().drop(["index","Type"],axis=1)
data2.head()

#split the set into training and test set
training_set_iris = data2.iloc[1:round(perc_train*len(data2)),:]
test_set_iris = data2.iloc[round(perc_train*len(data2)):,:]

#program the class itself
class perceptron(object):
    """
    Parameters
    ------------
    eta : determines the learning rate, float value
    

    Attributes
    -----------
    w_ : weight array
    """
    
    def __init__(self,eta = 0.01):
        self.eta = eta
        
    
    def fit(self,training_set,y):
        # initialize weights as an array of the length of the amount of columns in 
        # the training set plus one more for the w_0 weight
        self.w_ = np.zeros(training_set.shape[1]+1)
        for features_i, target in zip(training_set, y):
            update = self.eta*(target - self.predict(features_i))
            self.w_[0] += update
            self.w_[1:] += update * features_i
            
    def predict(self, set):
        index = self.w_[0] + np.dot(set, self.w_[1:])
        prediction = np.where(index > 0, 1, -1)
        return prediction
        
# initiate and train the model
x = perceptron(0.01)
x.fit(training_set_iris.iloc[:,0:2].values,training_set_iris.iloc[:,2].values)

# apply to the testing set 
evaluation = test_set_iris.copy()
evaluation.result = np.where(evaluation.loc[:,"Target"] == x.predict(test_set_iris.iloc[:,0:2]), "correct", "false")
evaluation












