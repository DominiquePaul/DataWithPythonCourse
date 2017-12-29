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
dq.columns

# We select columns 5 to 46 and send it to the
# vars() function that packages them as arguments
# for summarize_at().
# (Note, you can spell summarize with an s or z,
# R does not care, both functions do the same.)

x = vars(names(Dq)[5:46])


Dq = group_by(Dq,year, quarter) %>%
  summarize_at(x, mean)

# Note here some of the cool subtleties
# of R that make it a "functional" programming
# language. You can pass a function as an argument
# of a function: "mean" is a function that is an
# argument of summarize_at()!


# To show the power of functional programming,
# let's use another pair of functions.
# The code of the second line looks rather
# dense. I leave it to the experts among
# you to figure out how this works :-)
# For the others, it's good enough to 
# understand what the code DOES, not how
# it works.

x = vars(names(Dq)[3:44])

Dq <- Dq %>% mutate_at(x, funs(round(., 2)))

# Check out that we now have indeed quarterly data,
# calculated as the means over 3 consecutive months!

