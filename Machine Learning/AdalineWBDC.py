
# Description -------------------------------------------------------------

# ADALINE learning with WDBC data.

# Header ------------------------------------------------------------------

import os
import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt




# Parameters --------------------------------------------------------------

os.chdir("/Users/dominiquepaul/xJob/DataWithPythonCourse1/Machine Learning/")

eta = 0.01   # The learning rate

perc_train = 0.7 # Percentage of observations used for training



# Preparing Data  ------------------------------------------------------------

# replace this with your directory
wdbc = pd.read_csv("/Users/dominiquepaul/xJob/DataWithPythonCourse1/Data/wbdc.csv") 

# Select subset of our data
wdbc = wdbc.iloc[:,[1,2,5,10]]
wdbc["labels"] = wdbc.diagnosis.replace(["M","B"],[1,-1])

features = list(wdbc)[2:4]
target_var = "diagnosis"

# Standardization (with scikit learn)
wdbc[features[0]] = preprocessing.scale(wdbc[features[0]])
wdbc[features[1]] = preprocessing.scale(wdbc[features[1]])


# Reshuffling

wdbc = wdbc.sample(frac = 1, # determines the fraction of the values returned
                   random_state = 1).reset_index(drop = True) # set seed and reset index
         
                   
# We select a percentage of the sample for training
split = round(perc_train * len(wdbc))
train_set = wdbc[0:split]
test_set = wdbc[split:]

n_train = len(train_set)




# Initialize learning process (training) ---------------------------------------------

# empty list of indeces
indeces = np.zeros(n_train)

# empty matrix with our weights
weights = np.zeros((n_train, 3)) 

# More empty containers
misclass_list = np.zeros(n_train)
false_positives_list = np.zeros(n_train)
false_negatives_list = np.zeros(n_train)

# the initial weights, initialized at 0 (i.e. completely ignorant)
w = np.array([0.0,0.0,0.0])


# Learning/Training ----------------------------------------------------------------

for i in range(n_train):
    
    x_i = np.array(train_set[features].iloc[i])    # The x data from obs i
    
    y_i = np.array(train_set["labels"].iloc[i])     # The y data from obs i
    
    index_i = w[0] + w[1] * x_i[0] + w[2] * x_i[1]   
    # Note: other than R, Python is zero-indexed

    # The prediction for the current i, based on current weights
    pred_i = 1 if index_i >= 0 else -1
    
    # We are not only interested in the prediction to the current i
    # (which is used for updating the weights),
    # but how we would fare with the current i based on the ENTIRE training sample!
    
    train_set["index"] = w[0] + w[1] *train_set[features[0]] + w[2] * train_set[features[1]]
    train_set["prediction"] = np.where(train_set["index"] >= 0,1,-1)
    train_set["error"] = train_set["labels"] - train_set["prediction"]

    # Ratio of misclassified cases
    misclas = round(sum(train_set["error"] != 0) / len(train_set) * 100, 22)
    
    # False Positives
    x = np.where((train_set["prediction"] == 1) & (train_set["labels"] == -1),1,0)
    false_positives = round(sum(x) / len(train_set["labels"][train_set["labels"] == -1]) * 100, 1)
    
    # False Negatives
    x = np.where((train_set["prediction"] == -1) & (train_set["labels"] == 1),1,0)
    false_negatives = round(sum(x) / len(train_set["labels"][train_set["labels"] == 1]) * 100, 1)

    # Bookkeeping current w values, before they are updated
    weights[i] = w
    
    # Updating

    # !!!!! HERE IS THE ONLY DIFFERENCE TO PERCEPTRON LEARNING!!!!!!!!!!!!!!!
    
    w[1:] = w[1:] + eta * (y_i - index_i) * x_i    # updating the weights for the two features
    
    w[0] = w[0] + eta * (y_i - index_i)   # updating the constant/bias  
    
    # Bookkeeping: Filling the containers

    indeces[i] = index_i
    misclass_list[i] = misclas
    false_positives_list[i] = false_positives
    false_negatives_list[i] = false_negatives
     
 
weights = pd.DataFrame(weights)
weights["iter"]= np.arange(1,len(weights)+1)

Y = pd.DataFrame({"iter": np.arange(1,len(train_set)+1), "falPos": false_positives_list, "falNeg": false_negatives_list, "misclas": misclass_list})

result = pd.merge(Y, weights,on = "iter")

train_diag = ["false positives: " + str(false_positives), " false negatives: " + str(false_negatives), " misclas: "  + str(misclas)]
# Plotting the learning process (training) -------------------------------------------


plt.plot(result["iter"], result["misclas"], label = "Misclassified (all, in %)", c = "blue", alpha = 0.3)
plt.plot(result["iter"], result["falPos"], label = "False positives (in %)", c = "red", alpha = 0.3)
plt.plot(result["iter"], result["falNeg"], label = "False negatives (in %)", c = "black", alpha = 0.3)

plt.legend()
plt.grid()
plt.xlabel("Iteration")
plt.ylabel("Perc. of cases")
plt.suptitle("Adaline learning: Training (WDBC data)", size = 14)
plt.title(("Learning rate = ", eta, ", ", perc_train*100, " % of sample used for training"), size = 7)
#plt.savefig("plots/Adaline_training.png")
plt.show()


# Testing/evaluation ------------------------------------------------------

# Get the appropriate values for w
w = weights.iloc[n_train-1, 0:3]


# Calculate all the information needed for evaluation
# Note, we calculate a prediction for EVERY
# observation in the test data!

test_set["index"] = w[0] + w[1]*test_set[features[0]] + w[2]*test_set[features[1]]

test_set["prediction"] = np.where(test_set["index"] >= 0,1,-1 )

test_set["error"] = test_set["labels"] - test_set["prediction"]

# ratio of misclassified cases
misclas = round(sum(test_set["error"] != 0) / len(test_set) * 100, 2)

# False Positives
x = np.where((test_set["prediction"] == 1) & (test_set["labels"] == -1),1,0)
false_positives = round(sum(x) / len(test_set["labels"][test_set["labels"] == -1]) * 100, 1)

# False Negatives
x = np.where((train_set["prediction"] == -1) & (train_set["labels"] == 1),1,0)
false_negatives = round(sum(x) / len(train_set["labels"][train_set["labels"] == 1]) * 100, 1)

test_diag = ["false positives: " + str(false_positives), " false negatives: " + str(false_negatives), " misclas: "  + str(misclas)]

# The critical value for classifying a flower is
# w0 + w1x1 + w2x2 = 0. Solve this for x2:
# x2 = -w1/w2 x1 - w0/w2


# Create a preliminary plot

for label,df in test_set.groupby("labels"):
    plt.scatter(df["perimeterM"],df["concaveM"],c= df["diagnosis"])    
slope = -w[1] / w[2]
intercept = -w[0] / w[2]
abline_values = [slope * i + intercept for i in test_set["perimeterM"]]    
plt.plot(test_set["perimeterM"], abline_values, 'b')    
plt.show()



# A more sophisticated plot -----------------------------------------------

# No need to understand the details here!

 # Create a preliminary ggplot to get the axis ranges
fig, ax = plt.subplots()
ax.scatter(test_set["perimeterM"],test_set["concaveM"])
fig.show()

ylims = ax.get_ylim()
xlims = ax.get_xlim()

# For the background, generate a large data grid
xgrid = np.arange(xlims[0], xlims[1], (xlims[1] - xlims[0]) / 219.9)
ygrid = np.arange(ylims[0], ylims[1], (ylims[1] - ylims[0]) / 220)
nx = len(xgrid)
ny = len(ygrid)


xgrid = np.repeat(xgrid, ny)
ygrid = np.tile(ygrid, nx)
len(xgrid)
len(ygrid)

to_paint = pd.DataFrame(data = {"xgrid":xgrid, "ygrid":ygrid})
to_paint["index"] = w[0] + w[1] * xgrid + w[2] * ygrid
to_paint["prediction"] = np.where(to_paint["index"] >= 0,"1","-1")
to_paint["colour"] = np.where(to_paint["index"] >= 0,"#f79999","#9ed9f7")

# some comment amigo 

fig, ax = plt.subplots()
ax.set_xlim(xlims[0], xlims[1])
ax.set_ylim(ylims[0], ylims[1])
#ax.scatter(to_paint["xgrid"],to_paint["ygrid"], color = to_paint["prediction"] )
#ax.scatter(test_set["perimeterM"],test_set["concaveM"])
for label,df in to_paint.groupby("prediction"):
    ax.scatter(df["xgrid"],df["ygrid"], color=df["colour"], label =label)
for label,df in test_set.groupby("diagnosis"):
    ax.scatter(df["perimeterM"],df["concaveM"],c= df["diagnosis"], label =label)
    
ax.legend()
 
train_diag
test_diag

plt.savefig("plots/Adaline_training.png")
 
 
 
 

