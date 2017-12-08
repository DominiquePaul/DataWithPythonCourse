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
# %reset

# Load the packages
import pandas as pd
import os
from ggplot import aes, ggplot, geom_point, geom_line 

# set directory
os.chdir("/Users/dominiquepaul/xJob/4-New R translation/")

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
    
for row_nr in range(len(df)):
    if df["year"].astype(float) < 2007:
        df.loc[row_nr,"Period"] = 1
    else:
        df.loc[row_nr,"Period"] = 0
        
        
df["year"].astype(float) < 2007
        
df["Period"] = 1 if (df[["year"]] < 2007) else 0

df["year"].item()
    
D <- D %>% 
  mutate(Period = ifelse(year.astype(int)<2007, 1, 0))

ggplot(D) + 
  geom_point(aes(gEUR, Exp_All_R, color = Period))
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
