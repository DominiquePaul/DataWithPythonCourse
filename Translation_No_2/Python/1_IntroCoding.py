#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 15:14:42 2017

@author: dominiquepaul
"""



# Description -------------------------------------------------------------

# In this file, we have a look at some of the most basic concepts of
# programming: Variables and their types.
# You also see how it works to write code in a file (which you should always do).


# Header ------------------------------------------------------------------

# install.package
import pandas as pd
import numpy as np

# Variables and their types ----------------------------

a = 2
a

# See how a appears in the Environment pane?

b = 5

# Variables have types. Let's see what's
# the type of a...
type(a)


# Are there other types?
a_as_char = "a"
a_as_char

type(a_as_char)


# What is the difference?
a = 2
a == 2


# what is this?
h = a == 2


# or this?
k = a !=a_as_char

type(h)


# Combining single objects: Shopping Lists (1) -------------------------

shop_list = ["Milk (l)", "Cereals (packs)", "Qu\u00f6llfrisch (packs)"]

type(shop_list)


# Note, I included a so-called UTF-8 character:
"\u00f6"
# Check whether on your machine "ö" would work:
"ö"

# The problem is that it may work on your machine,
# but look weird on someone else's machine. So, to be 
# save, use UTF-8 encoding when using non-english letters.

# Other examples:

["\u00bc", "\u2135", "\u0024", "\u20ac"]


# Just google the encoding you need (e.g. "utf8 euro sign")



# shop_list is a vector. A vector is
# the basic unit of a variable in R
# even the variable a above was a vector 
# (of length 1)

# Check the length of shop_list
len(shop_list)


# Let's create some other vectors.

quant_list = [3, 2, 5]

price_list = [1.95, 2.05, 11.95]

shopping_data = pd.DataFrame(data = {'shop_list':shop_list, 'quant_list': quant_list, 'price_list': price_list})

shopping_data

# Instead of printing  "shopping_data" you can also just double-click
# on the object name under "Data" in the upper-right pane of Spyder (or whatever IDE you are using).

# so far we have only created lists, we cannot use these to do mathematical operations though
# for this we need to convert them to arrays via numpy
quant_list = np.array(quant_list)
price_list = np.array(price_list)

# lets check
type(quant_list)
type(price_list)


# now lets add the new column
shopping_data.assign(exp_per_item=quant_list * price_list)
shopping_data
#Hm, where is the new info?


# If we want to include the new variable in the 
# object shopping_data, we need to assign the updated
# object to that name!

shopping_data = shopping_data.assign(exp_per_item=quant_list * price_list)
shopping_data

# Three ways of getting rid of a colum

D1 = shopping_data.loc[:, # this means that we select all rows
["quant_list", "price_list"]] # this selects the columns we want


D2 = shopping_data.loc[:, # we again select all rows
shopping_data.columns != 'exp_per_item'] # we select all columns which are not "exp_per_item"
# This is far more elegant if you drop just a few columns!

# dropping a column by name
D3 = shopping_data.drop("shop_list", axis = 1)

# Now we also apply this to the shopping_data
shopping_data = shopping_data.loc[:,shopping_data.columns != 'exp_per_item']


# Now, we add again the exp_per_item column

shopping_data_aug = shopping_data.assign(exp_per_item=quant_list * price_list)

shopping_data_aug



# Lists -------------------------------------------------------------------

# A list is a general-purpose container that can contain any
# number and type of elements. For instance, a list can
# also contain a list...

# Here is an example

my_list = [ 
  shopping_data,
  np.array(range(1,11)), # the first argument assigns the start, the second the end
  np.array(range(6)),
  np.arange(2.0, 5.75, 0.25), # we use np.arrange(start, stop, steps) for floats
  shopping_data_aug
]

# different than in R, lists elements do not have key names but are indexed with numbers
# starting at 0. This means that the first element can be accessed by my_list[0]

my_list[0]

# In python we do not access a data frame or list with a dollar sign like this:
# shopping_data$price_list --> doesn't work
# instead we access a data frame through one of the following means:

shopping_data.loc[:,"price_list"] # loc searches by name, this returns a series
shopping_data.iloc[:,0] # iloc searches by index number, again starting with 0
shopping_data[["price_list"]] # this returns a data frame
shopping_data["price_list"] # this returns a series


# Dictionaries -------------------------------------------------------------------

# if we want to use keyword attributes to access our data, then
# we can also save the information as a dictionary

my_dict = {"firstEl": shopping_data, 
"secondEl": np.array(range(1,11)),
"thirdEl": np.array(range(6)),
"fourthEl": np.arange(2.0, 5.75, 0.25),
"fifthEl": shopping_data_aug
}

# we can then access our data as follows:
my_dict["thirdEl"]

# the difference is that the dictionary is unordered compared to the list




