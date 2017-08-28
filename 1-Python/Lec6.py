import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

# Set the working directory to the folder
# where you have the csv files from the SNB

os.chdir("/Users/dominiquepaul/xJob/1-DataWithPythonCourse/4-Data/")
# os.chdir("YOUR DIRECTORY")

# you might have to change the separator
rawXrates = pd.read_csv('dataXrates.csv', sep = ",") #, index_col = 0
rawAussen = pd.read_csv('aussenhandel_snb1.csv', sep = ",")

# we convert our non-numeric values to numbers
rawXrates.Value = pd.to_numeric(rawXrates.Value)
rawAussen.Value = pd.to_numeric(rawAussen.Value)

print(rawAussen.head())

# SET PARAMETERS HERE!
######################

startYear = 2000

curr = "EUR1"
# the currency examined, you can run
# rawXrates.D1.unique()
# to check for all possible values

tradeDir = "A"  
# Direction of trade               
# Values are E (Einfuhr)                 
# and A (Ausfuhr)                
# run rawAussen.D0.unique() for overview
 
goodsType = "MAE" 
# run rawAussen.D1.unique()

measure = "R" 
# run rawAussen.D2.unique()

a = rawXrates.iloc[0:20, :]
print(a)
a.head(-1)
a.tail(-1)

rawAussen.D0.unique()
rawAussen.D1.unique()
rawAussen.D2.unique()

# Functions
###########

def to_growth(series):
    #we have to reset the index as pandas will otherwise divide
    # all rows which have the same index, which would mean that all 
    # results would be zero
    out = (series.tail(-1).reset_index(drop = True) / series.head(-1) -1 ).reset_index(drop = True) * 100
    # This is one element shorter than input, 
    # add an NA as first value
    df1 = pd.DataFrame([None])
    # 'ignore_index' means that the two DFs are merged while neglecting 
    # any order of their indices 
    out = pd.concat([df1, out], ignore_index = True)
    return out

# Customize the data
####################

# A unique time identifier for BOTH data

rawXrates["year"] = pd.to_numeric(rawXrates["Date"].str[0:4])
rawXrates["month"] = pd.to_numeric(rawXrates["Date"].str[5:7])
rawXrates["timeID"] = rawXrates.year + (rawXrates.month -1) / 12

rawAussen["year"] = pd.to_numeric(rawAussen["Date"].str[0:4])
rawAussen["month"] = pd.to_numeric(rawAussen["Date"].str[5:7])
rawAussen["timeID"] = rawAussen.year + (rawAussen.month -1) / 12

# we subset our data

xrates = rawXrates[(rawXrates.D1 == curr) & (rawXrates.D0 == "M0") & 
          (rawXrates.timeID >= startYear)].loc[:, ["timeID", "D1", "Value"]]           

aussen = rawAussen[(rawAussen.D0 == tradeDir) & (rawAussen.D1 == goodsType) & 
                   (rawAussen.D2 == measure) & (rawAussen.timeID >= 
                   startYear)].loc[:, ["timeID", "D0", "D1", "D2", "Value"]]

                   
# Bring data into wide format
xrates_wide = xrates.pivot(index = "timeID", columns = "D1",  values = "Value")
print(xrates_wide.head()) 
# creating a joint column for each individual combination of D0, D1 and D2
aussen["join"] = aussen["D0"] + "_" + aussen["D1"] + "_" + aussen["D2"]
aussen_wide = aussen.pivot(index="timeID", columns="join", values = "Value")
print(aussen_wide.head())
# we explicitly do not reset our indexes yet because we will use them as a 
# reference to merge our data

#################################
# Merge the two data sets (NEW!!!!)
# DA stands for "Data for Analysis"

# both tables are joined together by their index which currently is 
# the timeID, look at the data and you will see that timeID is NOT a column
# but the index!

# if you only want to join rows where values for both DFs are present you can 
# use 'join = inner'
# axis means whether we want to merge them horizontally or vertically
# 0 means horizontal, 1 means vertical
DA = pd.concat([xrates_wide, aussen_wide], axis=1)
print(DA.head())
# we reset our index, thereby the index is pushed into the df as a new column 
DA = DA.reset_index()

# [FOR LATER] convert to growth rates
DA[curr] = to_growth(DA.loc[:, curr])
print(DA.head())


###########
# ANALYSIS
###########

# Variable name for exports/imports
print(DA.columns)
trade_col = tradeDir + "_" + goodsType + "_" + measure


# for convenience we define: 
x = DA[curr]
y = DA[trade_col]

# Make a plot
plt.plot(x, 
         y, 
         # NOTE: This code works for all types of export/import
         # data and exchange rates!!! They are captured in the 
         # variable names
         
         'b.', #color and form of the dots: 'b' => blue, '.' => dots
         ms = 5 # point size
         )  #The closing paranthesis

# labels x-axis
plt.xlabel(curr)
# labels y-axis
plt.ylabel(trade_col)
plt.show()


# add a OLS line of best fit (linear regression) 

# this checks which rows contain values that are and are not NaN values 
# because dont want to use these when calculating our OLS line
idx = np.isfinite(x) & np.isfinite(y)

# find the line of best fit with polyfit function of numpy, which returns
# us the y-intercept and slope
m,c = np.polyfit(x[idx], y[idx], 1)

# we plot the line:
plt.plot(x, 
         m*x + c,   # our y-values in the form of a linear equation
         'r-',      # a solid red line 'r' => red; '-' => solid line
         lw = 0.8   # set the line width
         ) 



# now lets run a regression and look at the mathematical results
# we again omit all rows containing NaN
results = smf.OLS(y[idx], x[idx]).fit()

# Inspect the results
print(results.summary())

# HOWEVER... It is more interesting to 
# look at how CHANGES in exchanges rates
# affect CHANGES in exports/imports

# How calculate changes?
test = pd.Series(range(1,11))
test.head(-1)
test.tail(-1)

d_test = (test.tail(-1).reset_index(drop = True)/test.head(-1).reset_index(drop = True) -1)*100
d_test

# in case your interested: you can test here what would
# happen if we wouldnt use 'reset.index(drop = True)'
# d_test_2 = (test.tail(-1) / test.head(-1) -1)*100           
# d_test_2              