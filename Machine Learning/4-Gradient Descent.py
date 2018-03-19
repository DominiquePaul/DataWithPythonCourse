#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 13:59:51 2018

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


# Hyperparameters

eta = 0.1
n_iter = 5




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
width = 1



# Now we calculate grids (matrices) with the values of the  
# cost function and the gradient



# Calculate the values of the cost function 
# and the gradients
############################################

w1 = w2 = np.arange(-w_lim-1, w_lim+1, width)

# we initialize our cost matrix
Z = np.zeros((len(w1), len(w2)))

# The values of the first and second element
# of the gradient, initialized as Zero
dcost1 = dcost2 = np.zeros((len(w1), len(w2)))


# this creates the grid which we will need for plotting later
X, Y = np.meshgrid(w1, w2)

# Our next task is to calculate the elements for cost and 
# Dcost1, Dcost2. For this we need the data since the values 
# depend on the data! For keeping things clean we copy the
# information we need from Data into a new data frame df
df = wdbc.ix[:,[features[0], features[1], "labels"]]


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
        
        # And calculate  the "scaled" errors, i.e. errors 
        # times the values of the features
        df["d1"] = -(df["labels"] - df["index"])*df[features[0]]
        df["d2"] = -(df["labels"] - df["index"])*df[features[1]]
        
        # The value of the cost function of the particular
        # grid point
        Z[x_,y_] = 0.5 * sum(df["error_sq"])
        
        # The values of the components of the gradient for
        # the particular grid point
        dcost1[x_,y_] = sum(df["d1"])
        dcost2[x_,y_] = sum(df["d2"])


# Rescale objective function such that derivatives 
# relate reasonably to w1,w2 scale (this is just rescaling everything)
# No need to understand this in detail.
shrink = (max(w1)-min(w2))/(Z.max() - Z.min())*10
   
Z = shrink*Z
dcost1 = shrink*dcost1
dcost2 = shrink*dcost2
 
# This returns the smallest value    
Z.min()

# Define a function that finds the position of the 
# minimum of cost in the matrix
def find_min(cost):
    location = np.unravel_index(np.argmin(cost, axis=None), cost.shape)
    return location

# Define function that finds value of cost or Dcost for 
# specific values of wvec
# (no need to understand the details)
def find_val(weights, mat):
    val = mat[np.where(w1 == weights[0])[0][0], np.where(w2 == weights[1])[0][0]]
    return(val)

# Check whether the function works
find_val((0,0), Z)


# THE ACTUAL GRADIENT DESCENT PROCEDURE
#######################################

# The first iteration
#####################

# Initial value and gradient
# (We choose a value that is far away from the minimum,
# thus, for once, not (0,0))
weights0 = np.asarray((9,9))

# Find value of the cost function 
# and of the gradients at this point
c0 = find_val(weights0, Z)
grad0 = np.asarray((find_val(weights0, dcost1), find_val(weights0, dcost2)))

# Apply the algorithm as indicated in the slides
# of Chapter 3 for a first iteration.
# Note the minus sign in the definition of D$d1 and D$d2
# above. Together with the minus sign in the updating formula
# below this yields a plus.
weights1 = weights0 - eta*grad0


# Also calculate the value of the cost function we would get to
# if we approximated it linearly by the gradient
# This useds some math you may not be too familiar with: 
# First-order Taylor approximations for a bivariate function.
# Just for those interested: The first derivatives are given
# by the gradient. And the distances (dx1, dx2) are given
# by eta*gradient. This explains the funny-looking square.
l1_lin = c0 - eta*sum(grad0*grad0)

# colInd defines a color scheme that we use incrementally.
# Initialize it to 1.
col_ind = 1



# Adding Arrows 

fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       alpha = 0.6, antialiased=False)
ax.plot([weights0[0], weights1[0]], [weights0[1], weights1[1]], [c0, l1_lin], color='red', alpha=0.8, lw=3)

plt.show()

# The new point is actually below the surface of the cost function,
# as we go down straight and the surface is concave.
# To get a point on the surface, we neeed to calculate the cost for the new
# values of w.

df["index"] = weights1[0]*df[features[0]] + weights1[1]*df[features[1]]
df["errorsq"] = (df["labels"] - df["index"])**2 

df["d1"] = -(df["labels"] - df["index"]) * df[features[0]]
df["d2"] = -(df["labels"] - df["index"]) * df[features[1]]

C1 = 0.5 * sum(df["errorsq"] * shrink)


# More iterations
#################


# We know build a function that just adds another arrow
# for another iteration.

# Call the starting value weightsOld
weights_old = weights1

# Define a function that adds another arrow/iteration
# This works exactly like the first iteration
# The arguments are the starting value for the iteration,
# and the the color used for the previous arrow

def add_iteration(weights_old, col_ind):
    
    df["index"] = weights_old[0]*df[features[0]] + weights_old[1]*df[features[1]]
    df["errorsq"] = (df["labels"] - df["index"])**2 

    df["d1"] = -(df["labels"] - df["index"]) * df[features[0]]
    df["d2"] = -(df["labels"] - df["index"]) * df[features[1]]
    
    cost = 0.5 * sum(df["errorsq"] * shrink)

    # The gradient, scaled with shrink factor
    grad = np.asarray((sum(df["d1"]), sum(df["d2"]))) * shrink
    
    # The UPDATE for this iteration
    weights_new = weights_old - eta * grad
  
    # The updated value of the cost function if calculated
    # with linear approximation using the gradient
    cost_new_lin = cost - eta * sum(grad * grad)
    

    # The new correct (not approximated) value of the cost function
    df["index"] = weights_new[0] * df[features[0]] + weights_new[1] * df[features[1]]
    df["errorsq"] = (df["labels"] - df["index"])**2 
    cost_new = 0.5 * sum(df["errorsq"]) * shrink

    # increment the color index
    col_ind +=  1
  
    
    # And finally add another arrow
    # Note that this is wrapped inside a try() function
    # The problem is that when the arrow gets tiny (very short)
    # r throws an error since it cannot properly draw the arrow
    # any more. The if{} below instructurs R to just do nothing
    # in this case. The arrow would be so small that we sould not 
    # see it anyway.
    #return(cost, cost_new_lin)
    ax.plot([weights_old[0], weights_new[0]],[weights_old[1], weights_new[1]],[cost, cost_new_lin], c= ("C" + str(col_ind)), alpha=0.8, lw=3)
    out = (weights_new, col_ind, cost_new)
    return(out)

# Call the function once 
out = add_iteration(weights_old, col_ind )


weights_old = out[0]
col_ind = out[1]
count = 1

# And call it as many times as indicated by nIter
while count <= n_iter:
    out = add_iteration(weights_old, col_ind)
    weights_old = out[0]
    col_ind = out[1]
    count += 1

# Add end point of iteration as a red square
ax.scatter(weights_old[0],weights_old[1], out[2], c = "red")

# Add the correct minimum as a green square
ax.scatter(w1[find_min(Z)[0]],w2[find_min(Z)[1]], Z.min(), c = "green")

# Give the entire 3D plot a title
fig.suptitle("Gradient descent for WDBC data")
#
## And add some text output, just for completeness
#print("\nThe minimum of the cost function is ", Z.min(), ".",
#"\nThe value currently achieved through gradient descent is ", out[2],".")


plt.show()














    
    
    
    
    
    
    
    



