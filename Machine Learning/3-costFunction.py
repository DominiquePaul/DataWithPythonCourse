#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 11:15:15 2018

@author: dominiquepaul
"""


# Description ------------------------------------------------------------

# Inspect shape of cost function for WDBC data with two features


# Header ------------------------------------------------------------------
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


# Preparations ------------------------------------------------------------
# replace this with your directory
wdbc = pd.read_csv("/Users/dominiquepaul/xJob/DataWithPythonCourse1/Data/wbdc.csv") 

# Select subset of our data
wdbc = wdbc.iloc[:,[1,2,5,10]]
wdbc["labels"] = wdbc.diagnosis.replace(["M","B"],[1,-1])

features = list(wdbc)[2:4]
target_var = "diagnosis"

# standardize the data (with scikit learn)
wdbc[features[0]] = preprocessing.scale(wdbc[features[0]])
wdbc[features[1]] = preprocessing.scale(wdbc[features[1]])

# These are the parameters for our grid
w_lim = 10
width = 0.5


# The cost function landscape ---------------------------

# The idea is to build a "grid" of all (w1, w2) values
# within a certain range bounded by the parameter wLim.
# w1vec and w2vec define the coordinates of our lanscape.
# On top of these we will build the error mountains and valley.
# The altitude of the error mountains will be indicated
# by the object cost. It contains an "altitude" for each
# coordinate (w1 x w2).


w1 = np.arange(-w_lim, w_lim, width)
w2 = np.arange(-w_lim, w_lim, width)

# we initialoze our cost matrix
Z = np.zeros((len(w1), len(w2)))

# this creates the grid which we will need for plotting later
X, Y = np.meshgrid(w1, w2)

# select a subset which we will need for our calculations
df = wdbc.ix[:,[features[0], features[1], "labels"]]

# Now we loop through the whole grid, defined by all 
# possible combinations of values from w1 and w2.
# (In mathematics, we would call the latter the Cartesian 
# product of w1 and w2). For each combination of the weights
# (w1, w2) we calculate the value of the cost function, which
# directly relates to the number of errors we would make
# if we applied the particular weights for our classification task
# (which means classifiying tumors as benign and malign).

for x_ in range(len(w1)):
    for y_ in range(len(w2)):
        
        # Calculate the value of the index this pair would 
        # lead to. Do so for EVERY observation/row in the data!!!undefined
        # So the result is an entire
        # column for every iteration in the loop!!! You can check this 
        # by setting k and h to particular values, e.g. (1,1).
        df["index"] = w1[x_] * df[features[0]] + w2[y_] * df[features[1]]
        # Calculate the squared error for every row
        df["error_sq"] = np.square(df["labels"] - df["index"])
        # The value of the cost function is the sum over all 
        # rows, multiplied by one half
        loss = 0.5 * sum(df["error_sq"])
        # Write the result into the appropriate cell of the cost matrix
        Z[x_,y_] = loss

    
# This returns the smallest value    
Z.min()
# This returns the location of the smallest value as tuple
location = np.unravel_index(np.argmin(Z, axis=None), Z.shape)



# Interactive 3D plot -----------------------
        
# This code, as well as an explanation, can be found at 
# https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html
# Under the name "surface plots"

# Create plot of the error landscape (a 3D object)
fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       alpha = 0.8, antialiased=False)

# add a marcation of the minimum 
ax.scatter(w1[location[0]],w2[location[1]],Z.min(), c = "red")

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()



























