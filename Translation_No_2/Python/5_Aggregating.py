#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 23:12:12 2017

@author: dominiquepaul
"""

# Description -------------------------------------------------------------

# Sometimes, you have data in "fine resolution" and you need it actually
# at a more "aggregate" resolution. For instance, you may have montly
# data, but you actually need quarterly data (e.g. because you want
# to combine your data with other data where you only have quarterly
# information).

# In this script, we are having a look on how to do that.
# You can read more on this in the book in Chapter 3.


# Packages ------------------------------------------------------------------

import pandas as pd
import numpy as np
import os

#%reset
# Header ------------------------------------------------------------------

# set directory
os.chdir("/Users/dominiquepaul/xJob/DataWithPythonCourse1/Translation_No_2/")

d = pd.read_pickle("Data/TradeEx_tidy.pkl")



# Aggregating to quarterly data -------------------------------------------

# Calculate quarter


# We create a new dataframe Dq with quarterly data.
# We use the cut function that transforms a continuous
# range into a categorical variable
dq = d
dq["quarter"] = pd.cut(dq["month"], bins=[0, 3.5, 6.5, 9.5, 13], labels=[1,2,3,4])

type(dq["quarter"][0])

# dropping some columns to improve legibility
dq = dq.drop(['month', 'date_num'], axis = 1)



# To see how the cut function works, consider 
check_it_out = pd.cut(np.arange(1,13,1),bins=[0, 3.5, 6.5, 9.5, 13], labels=[1,2,3,4])
check_it_out


# The next step is to "group" the data by quarters.
# Well, actually not by quarters, but by all possible
# combinations of years and quarters. (What's the difference?)

# The book only discusses summarise with hand-picked
# single columns. Here, we want to summarise a large 
# number of columns. So we use the summarise_at()
# function that allows us to exactly do this.


# Get a list of all column names
len(dq.columns)


dq = dq.groupby(["year","quarter"]).mean().reset_index().iloc[:,:44]


# We select columns 5 to 46 and summarize the columns by the periods
# we group the values by taking their average and reset the index 
# finally, we only select the columns we are interested in


# we round the values to again improve legibility
dq = dq.round(decimals = 2)

# Check out that we now have indeed quarterly data,
# calculated as the means over 3 consecutive months!



# Changing order of columns -----------------------------------------------

# Finally, let's explore how we can change the order of columns. 

# Get the list of all column names
dq.columns

# Selecting the columns that we want to have 
# left-most, ordered appropriately
first = list(dq.columns[0:2]) + list(dq.columns[42:44]) + list(dq.columns[2:42])

# Then using reindex() to rearange
dq = dq.reindex(columns = first)























