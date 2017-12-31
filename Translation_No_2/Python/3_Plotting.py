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
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import scipy.stats
import numpy as np
 
# set directory
os.chdir("/Users/dominiquepaul/xJob/DataWithPythonCourse1/Translation_No_2/")

# Load the data that we prepared in 2_DataBasics.R
df = pd.read_pickle("Data/TradeEx_tidy.pkl")





# Plotting basics ----------------------------------------------------------------

# What (statistical) variables do we have?
df.columns

# A simple scatterplot
plt.scatter(df["gEUR"], df["Exp_All_R"])
plt.show()

# Give separate color to observations before 2007 ------------------

# Here is a possible solution

# Create a new so-called "indicator variable". 
# For this, the ifelse() function is very convenient.
   
df.loc[:,"Period"] = 0
df.loc[df["year"] < 2007, "Period"] = 1
    

plt.scatter(df["gEUR"], df["Exp_All_R"],
            c = df["Period"],  #adjusts the color depending on a third variable
            s = 4, # size of the dots
            cmap='bwr' # color map of the dots, in our case blue and red
            # check out more schemes here: 
            #http://matplotlib.org/examples/color/colormaps_reference.html
            )
plt.show()
   
        
# Adding a legend -------------------------------------------------


# There are two methods of doing this:

# The first one is rather basic
# we create our own legend through so-called patches 
red_patch = mpatches.Patch(color = "red",label = "Before 2007")
blue_patch = mpatches.Patch(color = "blue",label = "After 2007")
labels = [red_patch,blue_patch]

plt.scatter(df["gEUR"], df["Exp_All_R"],c = df["Period"],s = 4,cmap='bwr')
plt.legend(handles=labels)
plt.show()


# Axis labels --------------------------------------------

plt.scatter(df["gEUR"], df["Exp_All_R"],c = df["Period"],s = 4,cmap='bwr')
plt.legend(handles=labels)
plt.xlabel("Change of CHF/Euro exchange rate (in %)")
plt.ylabel("Change in total exports (in %)")
plt.show()

xlab1 = "Change of CHF/Euro exchange rate (in %)"
ylab1 = "Change in total exports (in %)"


# other options with MPL:

# we can also change the size of the dots depending on a third factor: 
# in our case we will use the chemistry exports column to be able to 
# see when this might have had an impact on our results

# we can also make our colours continuous depending on the date of the data pair

plt.scatter(df["gEUR"], df["Exp_All_R"],c = df["date_num"],s = df["Exp_Chemistry_R"]*10,cmap='YlGn', alpha= 0.5)
light_patch = mpatches.Patch(color = "#fafcdd",label = "2001")
dark_patch = mpatches.Patch(color = "#7fa294",label = "2017")
labels = [light_patch,dark_patch]
plt.legend(handles=labels)
plt.xlabel("Change of CHF/Euro exchange rate (in %)")
plt.ylabel("Change in total exports (in %)")
plt.show()

# reset patches
red_patch = mpatches.Patch(color = "red",label = "Before 2007")
blue_patch = mpatches.Patch(color = "blue",label = "After 2007")
labels = [red_patch,blue_patch]



# Visualizing statistical relationship between two variables ------------------

### LINEAR REGRESSION COMES HERE ###
# Lets do a classical linear regression with intercept and slope

# we can make a regression using the scipy package (very import for machine learning)
reg1 = scipy.stats.linregress(df["gEUR"], df["Exp_All_R"])
reg1.pvalue
# however it is not working. Why?
df["gEUR"].head()
# looking at the data we see we have a nan values, which stop scipy from making a regression
# we can easily elimiate these with a mask though

# ~is the same as "is not" as we are looking for the rows were both columns have a value unequal to nan
mask = ~np.isnan(df["gEUR"]) & ~np.isnan(df["Exp_All_R"])
reg1 = scipy.stats.linregress(df["gEUR"][mask], df["Exp_All_R"][mask])
# we get an object with containg multiple attributes regarding our regression analysis

# we need the slope and the intercept:
slope, intercept = reg1[0], reg1[1]


plt.scatter(df["gEUR"], df["Exp_All_R"],c = df["Period"],s = 4,cmap='bwr')
plt.plot(df["gEUR"], intercept + slope * df["gEUR"])
plt.legend(handles=labels)
plt.xlabel("Change of CHF/Euro exchange rate (in %)")
plt.ylabel("Change in total exports (in %)")
plt.show()





# If you want to add a title and some other text

plt.scatter(df["gEUR"], df["Exp_All_R"],c = df["Period"],s = 8,cmap='bwr' )
plt.legend(handles=labels)
# labels, title, caption
plt.xlabel(xlab1)
plt.ylabel(ylab1)
plt.suptitle("Surprisingly little effect", fontsize = 13) # add the big title
plt.title("Swiss exports and the CHF/euro exchange rate", fontsize=10) # add a subtitle
plt.text(0, -40, "Data source: Swiss National Bank") # add a textbox with further annotations
# the first two argument are the x and y coordinates of the text
plt.show()


# Changing the background and other features -------------------------------------------------



# If you do not like the background you can change the theme
# check out different themes here:
# https://matplotlib.org/gallery/style_sheets/style_sheets_reference.html?highlight=style%20context

# the with command allows us to maintain a certain style only for a certain block of code
# this way we dont have to reset the theme after using it once, in case we dont like it
# amusingly, ggplot is one of the availabel themes

with plt.style.context(('ggplot')): 
    plt.scatter(df["gEUR"], df["Exp_All_R"],c = df["Period"],s = 8,cmap='bwr' )
    plt.legend(handles=labels)
    # labels, title, caption
    plt.xlabel("Change of CHF/Euro exchange rate (in %)")
    plt.ylabel("Change in total exports (in %)")
    plt.suptitle("Surprisingly little effect", fontsize = 13) # add the big title
    plt.title("Swiss exports and the CHF/euro exchange rate", fontsize=10) # add a subtitle
    plt.text(0, -40, "Data source: Swiss National Bank") # add a textbox with further annotations
    # the first two argument are the x and y coordinates of the text
    plt.show()




# Saving plots ------------------------------------------------------------


# First create a new folder Plots inside your standard working directory!    
    
with plt.style.context(('ggplot')): 
    plt.scatter(df["gEUR"], df["Exp_All_R"],c = df["Period"],s = 8,cmap='bwr' )
    plt.legend(handles=labels)
    # labels, title, caption
    plt.xlabel("Change of CHF/Euro exchange rate (in %)")
    plt.ylabel("Change in total exports (in %)")
    plt.suptitle("Surprisingly little effect", fontsize = 13) # add the big title
    plt.title("Swiss exports and the CHF/euro exchange rate", fontsize=10) # add a subtitle
    plt.text(0, -40, "Data source: Swiss National Bank") # add a textbox with further annotations
    # the first two argument are the x and y coordinates of the text
    plt.savefig("Plots/ello.png")
    plt.savefig("Plots/ello.pdf")



# Regressions -------------------------------------------------------------


# as mentioned above: we can use regression analysis to extract useful information from our data
mask = ~np.isnan(df["gEUR"]) & ~np.isnan(df["Exp_All_R"])
reg1 = scipy.stats.linregress(df["gEUR"][mask], df["Exp_All_R"][mask])

# but this data contains more than just the slope and intercept for a regression line
# we can either print out everything at once:
reg1
# or access single attributes on their own (e.g. for further computation)
reg1.pvalue

# # Another (prettier option) is the statsmodels package
# import statsmodels.formula.api as smf
# results = smf.OLS(df["gEUR"][mask], df["Exp_All_R"][mask]).fit()
# # Inspect the results
# print(results.summary())


# We will talk more about regression output in the context of R Markdown

  

  
  
  
  
  
  
  
  
  
