#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 12:56:32 2018

@author: dominiquepaul
"""

"""
perceptron 2.0:
this version of the code *INCLUDES* a bookkeeping file which tracks 
the development of model as it passes through several iterations
"""


# This script serves to explain the perceptron algorithm in Python. As a second 
# step we will use the code to create an object in python to make further use easy


# we import our packages
from sklearn import datasets
from sklearn.utils import shuffle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

eta = 0.01
perc_train = 0.7 # the training set size as percentage of overall set

# Prepare data for use --------------------------------------------------------------

# The data we will be using is a data set on flowers called Iris. A thorough 
# explanation of the data set can be found on wikipedia or other sources:
# https://en.wikipedia.org/wiki/Iris_flower_data_set

# we load the data set
iris = datasets.load_iris()
# we extract the data frame from the object containing the relevant information
# and select the sepal and petal width in columns 2 and 4 
data = pd.DataFrame(iris.data).iloc[:,[1,3]]
 
# we join this data with the labels on the actual species into one data frame
data = data.join(pd.DataFrame(iris.target))
# rename columns
data.columns = ["Sepal_length", "Petal_length","Target"]


# we add a new column for string labeling to make things easier for us
data["Type"] = data["Target"]
data["Type"].replace([0,1,2], ["Setosa","Versicolor","Virginica"], inplace = True)

# For now we are only interested in the Setosa and Versicolor data. We omit Virginica
data1 = data.loc[data.loc[:,"Type"].isin(["Setosa","Versicolor"])]

# we change the label so that we either have -1 or 1 as a label instead of 0 and 1
data1["Target"].replace([0],[-1], inplace=True)
data1

# This data set is ordered. To create a more realistic learning environment 
# we will shuffle the rows using the shuffle function from sklearn
data2 = shuffle(data1, random_state = 1).reset_index().drop(["index","Type"],axis=1)
# checking:
data2.head()

# we now split the set into a training and test set. We will use the test set to
# evaluate how good our algorithm performs
# perc_train states how much percent of the data shall be allocated for testing
training_set_iris = data2.iloc[0:round(perc_train*len(data2)),:]
test_set_iris = data2.iloc[round(perc_train*len(data2)):,:]

# our data is now prepared and we can continue to apply our algorithm
# Create the class for our ML object ------------------------------------------

# we start off by writing a small function which based on an input of weights can 
# give us a prediction 
def predict(weights_input, features_input):
    # index is the exact numeric prediction of the prediction function
    # np.dot multiplies the two vectors with each other (one of them being transposed)
    index = weights_input[0] + np.dot(features_input, weights_input[1:])
    # we round our preiction to a value of either 1 or -1. Predictions are absolute
    # there is no such thing as a prediction corresponding to "probably" Versitosa
    # It is either a 100% yes or no 
    prediction = np.where(index > 0, 1, -1)
    return prediction
        



# we initialize our weights vector with 0s. The size of the vector is given by 
# the number of features in our training data + 1 in order to account for the 
# first weight w_0 which does not pertain to a feature
# the method we use to arrive at this number is a bit more complicated but you will see
# why later. 
weights = np.zeros(training_set_iris.iloc[:,0:2].values.shape[1]+1)

# a data frame which we will use to keep track of some attributes during the learning process
bookkeeping_df = pd.DataFrame(index = np.arange(0,70,1), columns = ["iter", "misclas","false_positives","false_negatives"])
# a data frame to keep track of the development of the weights during the learning process
weights_df = pd.DataFrame(0,index = np.arange(0,70,1), columns = range(3))

# we initiate a variable to keep track of our iterations
iteration = 1

# we may now start iterating through our training set and fitting our weights

# we run a for loop. using the zip function allows us to iterate through two 
# different variables at the same time. 
# features_i is a vector containing the feature values 
# and target represents the labels which are an integer (either -1 or 1) 
for features_i, target in zip(training_set_iris.iloc[:,0:2].values, training_set_iris.iloc[:,2].values):
    
    # the main part is updating the weights, this is quite straightforward
    update = eta*(target- predict(weights, features_i))
    weights[0] += update
    weights[1:] += update * features_i
    
    # in a second step we record changes of the values for our bookkeeping
    
    bookkeeping_df.ix[iteration-1,"iter"] = iteration
    
    # we calculate the percentage amount of mistakes by applying our new weights to the
    # entire training data set and checking how the estimates compare to the actual labels
    mistakes = sum(np.where(training_set_iris.iloc[:,2].values == predict(weights, training_set_iris.iloc[:,0:2].values),0,1))/len(training_set_iris)
    bookkeeping_df.ix[iteration-1, "misclas"] = mistakes
    
    # we also count the false positives
    # false positives
    false_positives = sum(np.where((predict(weights, training_set_iris.iloc[:,0:2].values) == 1) & (training_set_iris.iloc[:,2].values == -1) ,1,0))/ np.sum(np.array(training_set_iris.iloc[:,2].values) == -1) 
    bookkeeping_df.ix[iteration-1,"false_positives"] = false_positives
    # false negatives
    false_negatives = sum(np.where((predict(weights, training_set_iris.iloc[:,0:2].values) == -1) & (training_set_iris.iloc[:,2].values == 1),1,0))/ np.sum(np.array(training_set_iris.iloc[:,2].values) == 1)
    bookkeeping_df.ix[iteration-1,"false_negatives"] = false_negatives

    # we also adjust our data frame keeping track of the weights
    for m in range(len(weights)):
        weights_df.ix[iteration-1, m] = weights[m]
        
    # this is the last part of our loop, we record that we have completed the iteration
    iteration += 1
    

# after completing the loop we now merge the two bookkeeping data frames. As you can 
# deduct from the code above it was easier keeping them separate so far

bookkeeping_df = bookkeeping_df.join(weights_df)


#######################################
# Thats it! We can now continue to compare our fit to the testing set which we created earlier
#######################################

    
# apply to the testing set 
evaluation = test_set_iris
evaluation["result"] = np.where(evaluation["Target"] == predict(weights, test_set_iris.iloc[:,0:2]), "correct", "false")
evaluation

# now imagine we would have another data set which we would like to apply this
# algorithm to. We would have to exchange many variables and this would take a lot of time
# Instead, we can simply create an object in python. 
# In this object we will be able to create methods of the object. In our case we can 
# use our predict function as well as create a "fit" method which will adapt the object
# to the data at hand. This way we can create multiple objects at the same time

# So lets create an object. You will notice that while most things are the same, 
# there are some minor differences
    
# variables which are created after initiation are marked with a "_" as a suffix

# variables are "owned" by the object and are referenced by self.variable_name

# Creating methods for the object is just like creating a function with the difference that
# the first argument is "self"

# the method "__init__"  is called automatically when we create an instance of the object
# later on. Here we define all relevant variables (/attributes) of the object


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
    
    eta = 0.01
    
    def __init__(self,eta):
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
        
    
    

#######################################
# Testing the algorithm as an object
#######################################

# now where we created the object we can apply it to the same use as our manually 
# created approach earlier:

# initiate and train the model
x = perceptron(0.01)
x.fit(training_set_iris.iloc[:,0:2].values,training_set_iris.iloc[:,2].values)

# apply to the testing set 
evaluation = test_set_iris
evaluation["result"] = np.where(evaluation["Target"] == x.predict(test_set_iris.iloc[:,0:2]), "correct", "false")
evaluation

# examine the development over time
x.bookkeeping_


# examine development of weights via graph
plt.plot(x.bookkeeping_["iter"], x.bookkeeping_.ix[:,4])
plt.plot(x.bookkeeping_["iter"], x.bookkeeping_.ix[:,5])
plt.plot(x.bookkeeping_["iter"], x.bookkeeping_.ix[:,6])
plt.title("Development of the weights")
plt.xlabel("Iterations")
plt.ylabel("Values")
plt.grid()
plt.legend()
plt.show()















