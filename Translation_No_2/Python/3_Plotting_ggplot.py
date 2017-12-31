#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 18:06:25 2017
@author: dominiquepaul
"""


# Description -------------------------------------------------------------

# In this script, we are going to dive deeper into the
# plotting options



# Header ----------------------------------------------------------------

# The header contains all the preparatory stuff

# Start with a clean sheet
#%reset


# Load the packages
import pandas as pd
import os
from ggplot import * 
#from ggplot import aes, ggplot, geom_point, geom_line, labs 

# set directory
os.chdir("/Users/dominiquepaul/xJob/DataWithPythonCourse1/Translation_No_2")

# Load the data that we prepared in 2_DataBasics.R
df = pd.read_pickle("Data/TradeEx_tidy.pkl")





# Plotting basics ----------------------------------------------------------------

# What (statistical) variables do we have?
df.columns

# A simple scatterplot
ggplot(df, aes(x = "gEUR", y = "Exp_All_R")) +\
    geom_point()

# Give separate color to observations before 2007 ------------------

# Here is a possible solution

# Create a new so-called "indicator variable". 
# For this, the ifelse() function is very convenient.
   
df.loc[:,"Period"] = 0
df.loc[df["year"] < 2007, "Period"] = 1
    
        
ggplot(aes("gEUR", "Exp_All_R", color = "Period"), df) +\
    geom_point()


# Factors and visualizing group membership -------------------------------------------------


# It does not look too bad, but the legend reveals that
# Python ggplot does not quite exactly what we want...

type(df["Period"][0])
# Period is a numerical variable

# We actually want Period to be a categorical variable.
# That's something else than just character. 
# As you may imagine, there is a data type for this.

# For this, we use the forcats package (see header).
# Read about this in Chapter 12.

df.loc[:,"Period"] = False
df.loc[df["year"] < 2007, "Period"] = True
    
        
ggplot(aes("gEUR", "Exp_All_R", color = "Period"), df) +\
    geom_point()

# This looks more like what we wanted!


# Let's make the legend nicer
# Factors have the options to give labels to the categories. It's those
# labels that are used for the legend!
    
df.loc[:,"Period"] = "After 2007"
df.loc[df["year"] < 2007, "Period"] = "Before 2007"
    
        

ggplot(aes("gEUR", "Exp_All_R", color = "Period"), df) +\
    geom_point() 



# Axis labels --------------------------------------------

ggplot(aes("gEUR", "Exp_All_R", color = "Period"), df) +\
    xlab("Change of CHF/Euro exchange rate (in %)") +\
    ylab("Change in total exports (in %)") +\
    geom_point()



# Visualizing statistical relationship between two variables ------------------
# At this point the ggplot package starts failing to live up to our needs:
    
# The regression fails because the ggplot package isnt updated anymore and the new pandas 
# update has omitted a function on which this section relied
# for this reason we do not use ggplot anymore. If you like,
# you can of course install an older version of pandas to make this run
    
# other parts are either not implemented or not documented well online so we 
# we stop here and continue with Matplotlib (see other script)
    
# this is the code we would have run but which does not work

xlab1 = "Change of CHF/Euro exchange rate (in %)"
ylab1 =  "Change in total exports (in %)"

ggplot(aes("gEUR", "Exp_All_R", color = "Period"), df) +\
    xlab(xlab1) +\
    ylab(ylab1) +\
    geom_point() +\
    stat_smooth(method='loess')

