"""
perceptron 2.0:
this version of the code *INCLUDES* a bookkeeping file which tracks
the development of model as it passes through several iterations
"""

from sklearn import datasets
from sklearn.utils import shuffle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


perc_train = 0.7 # the training set size as percentage of overall set

# Prepare data for use --------------------------------------------------------------

iris = datasets.load_iris()
data = pd.DataFrame(iris.data).iloc[:,[1,3]]

# add column with the classification labels
data = data.join(pd.DataFrame(iris.target))
# rename columns
data.columns = ["Sepal_length", "Petal_length","Target"]


# add new column for text labelling of flower
data.loc[:,"Type"] = data.loc[:,"Target"]
data.loc[:,"Type"].replace([0,1,2], ["Setosa","Versicolor","Virginica"], inplace = True)

# Delete all virginica rows
data1 = data.loc[data.loc[:,"Type"].isin(["Setosa","Versicolor"])].copy()

#
data1["Target"].replace([0],[-1], inplace=True)
data1

#shuffle data set
data2 = shuffle(data1, random_state = 1).reset_index().drop(["index","Type"],axis=1)
data2.head()

#split the set into training and test set
training_set_iris = data2.iloc[0:round(perc_train*len(data2)),:]
test_set_iris = data2.iloc[round(perc_train*len(data2)):,:]


# Create the class for our ML object ------------------------------------------


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
            self.bookkeeping_.loc[self.iteration-1,"iter"] = self.iteration
            mistakes = sum(np.where(y == self.predict(training_set),0,1))/len(training_set)
            self.bookkeeping_.loc[self.iteration-1,"misclas"] = mistakes

            # false positives
            false_positives = sum(np.where((self.predict(training_set) == 1) & (y == -1) ,1,0))/ np.sum(np.array(y) == -1)
            self.bookkeeping_.loc[self.iteration-1,"false_positives"] = false_positives
            # false negatives
            false_negatives = sum(np.where((self.predict(training_set) == -1) & (y == 1),1,0))/ np.sum(np.array(y) == 1)
            self.bookkeeping_.loc[self.iteration-1,"false_negatives"] = false_negatives

            for i in np.arange(0,training_set.shape[1]+1,1):
                self.weightsdf_.loc[self.iteration-1,i] = self.w_[i]

            self.iteration += 1

        self.bookkeeping_ = self.bookkeeping_.join(self.weightsdf_)

    def predict(self, set):
        index = self.w_[0] + np.dot(set, self.w_[1:])
        prediction = np.where(index > 0, 1, -1)
        return prediction



# use the class ---------------------------------------------------------------
 
# initiate and train the model
x = perceptron(0.01)
x.fit(training_set_iris.iloc[:,0:2].values,training_set_iris.iloc[:,2].values)

# apply to the testing set
evaluation = test_set_iris.copy()
evaluation["result"] = np.where(evaluation["Target"] == x.predict(test_set_iris.iloc[:,0:2]), "correct", "false")
evaluation

# examine the development over time
print(x.bookkeeping_)


# # examine development of weights via graph
# plt.plot(x.bookkeeping_["iter"], x.bookkeeping_.loc[:,4])
# plt.plot(x.bookkeeping_["iter"], x.bookkeeping_.loc[:,5])
# plt.plot(x.bookkeeping_["iter"], x.bookkeeping_.loc[:,6])
# plt.title("Development of the weights")
# plt.xlabel("Iterations")
# plt.ylabel("Values")
# plt.grid()
# plt.legend()
# plt.show()
