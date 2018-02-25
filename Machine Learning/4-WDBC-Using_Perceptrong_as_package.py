#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 10:42:33 2018

@author: dominiquepaul
"""
"""
In this script we will learn to import our perceptron code as a package and run 
it using an other data set, the wdbc data set.

For this we first of all create a python file called "perceptron2_as_package.py" 
where we have deleted all code related to the iris set and only the code defining 
the class perceptron remains.

Additionally we add a small function called "test_package" which does nothing else 
than print "test worked" so we can test whether our package import worked
"""
# first, we import all our packages as usual
import pandas as pd
from sklearn.utils import shuffle
import numpy as np

# We also import the os package to set our working directory to the directory where 
# our perceptron package is located
import os
os.chdir("/Users/dominiquepaul/xJob/DataWithPythonCourse1/Machine Learning/own_packages")

# we can now import our package
import perceptron2_as_package as perc


# lets test if it worked
perc.test_package()

# we may now prepare our wdbc data to make it suiting to our work:
wdbc = pd.read_csv("/Users/dominiquepaul/xJob/DataWithPythonCourse1/Data/wbdc.csv")
wdbc.replace(["M","B"],[0,1], inplace = True)

perc_train = 0.7

# shuffle the data set
wdbc = shuffle(wdbc, random_state = 1).reset_index().drop(["index"],axis=1)

#split the set into training and test set
training_set_wdbc = wdbc.iloc[0:round(perc_train*len(wdbc)),:]
test_set_wdbc = wdbc.iloc[round(perc_train*len(wdbc)):,:]


                          
######################################################
# This is the part where we start using our own package!
######################################################

# we can easily reference the object and create an instance as follows:
x = perc.perceptron(0.01)
x.fit(training_set_wdbc.iloc[:,3:33].values, training_set_wdbc.iloc[:,2].values)
 
# Thats it! using the code as a package saves us a lot of time!

# Lets check how well the perceptron algorithm performs on the wdbc data
evaluation = test_set_wdbc
evaluation["result"] = np.where(evaluation.iloc[:,2] == x.predict(test_set_wdbc.iloc[:,3:33].values), 1, 0)
corrects = evaluation["result"].sum()
estimations_made = len(evaluation["result"])
fraction_correct = corrects / estimations_made
print("The Perceptron algorithm classified {0:.3f}% of the test data correctly".format(fraction_correct))



