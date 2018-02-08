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
import scipy.stats
import matplotlib as mpl
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

# There are twoi methods to create a legend


# the first method works by manually assigning the labels for the legend
# Normally the legend handle (the sign in the legend) and legend label (text)
# are automatically assigned when plotting and can then be called via
# the plt.legend() function. 
# We change the plotted legend by manually assigning the legend handles

# in this line we create an empty plot which we use to reference as constituting 
# the information of the legend to be called later
handle_before_2007 = plt.scatter([],[], color='r', label = "Before 2007")
handle_after_2007 = plt.scatter([],[], color='b', label = "After 2007")

# we save our individual patches as a list so we can easily 
# reference them later
labels = [handle_before_2007,handle_after_2007]

plt.scatter(df["gEUR"], df["Exp_All_R"],c = df["Period"],s = 4,cmap='bwr')
plt.legend(handles=labels)
plt.show()


# The second method is the automatic but more complicated way
# we plot the dots in iterations depending on their period labelling
df.loc[:,"Period2"] = "After 2007"
df.loc[df["year"] < 2007, "Period2"] = "Before 2007"    

groups = df.groupby('Period2')
for name, group in groups:
    plt.scatter(group.gEUR, group.Exp_All_R, label = name)
plt.legend()

df = df.drop("Period2", axis = 1)


# Axis labels --------------------------------------------

plt.scatter(df["gEUR"], df["Exp_All_R"],c = df["Period"],s = 4,cmap='bwr')
plt.legend(handles=labels)
plt.xlabel("Change of CHF/Euro exchange rate (in %)")
plt.ylabel("Change in total exports (in %)")
plt.show()



# we save our axes labels once so we dont have to type them every time
xlab1 = "Change of CHF/Euro exchange rate (in %)"
ylab1 = "Change in total exports (in %)"




# other options with MPL:

# we can also change the size of the dots depending on a third factor: 
# in our case we will use the chemistry exports column to be able to 
# see when this might have had an impact on our results

# we make our colours continuous depending on the date of the data pair
# and change the opacity of the dots with the alpha value

# We will also create a colour bar on the side
# you can read the exact instructions here: 
# https://matplotlib.org/examples/api/colorbar_only.html

# first split our plot into subplots:
# we call them ax1 and ax2
# we split our plotting space into a 10x10 matrix and define how we want to 
# allocate the space for the two subplots
# read more here: https://matplotlib.org/users/gridspec.html
ax1 = plt.subplot2grid((10, 10), (0, 0), colspan=8, rowspan=10)
ax2 = plt.subplot2grid((10, 10), (0, 9), colspan=1, rowspan= 10)

# we can now plot the data. The procedure is the same. 
# We merely replace "plt" with "ax1"
ax1.scatter(df["gEUR"], 
            df["Exp_All_R"],
            c = df["date_num"],
            s = df["Exp_Chemistry_R"]*5,
            cmap='YlGn', 
            alpha= 0.5)

# we will now create our legend as a colourbar to show the continous data

cmap = mpl.cm.YlGn #this sets our chosen color map type
# we normalize our the colour bar values according to our data
norm = mpl.colors.Normalize(vmin=min(df["date_num"]), vmax=max(df["date_num"]))

# create the colour bar: 
cb1 = mpl.colorbar.ColorbarBase(ax2, # where do we plot to
                                cmap=cmap, # which colour map we are using
                                norm=norm, # normalized data
                                orientation='vertical') # orientation
# optional: set a label to the legend
# cb1.set_label('Date of data')
plt.show()


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

# we save our original data frame and copy selected columns where 
# we then drop all nan values. This is needed for the regression function
df_original = df
df = df_original[["gEUR","Exp_All_R","Period"]]
df = df.dropna(axis = 0, how = "any")

reg1 = scipy.stats.linregress(df["gEUR"], df["Exp_All_R"])
# we get an object with containg multiple attributes regarding our regression analysis

# we need the slope and the intercept:
slope, intercept = reg1[0], reg1[1]


# lets plot our regression analysis onto the scatter plot
plt.scatter(df["gEUR"], df["Exp_All_R"],c = df["Period"],s = 4,cmap='bwr')
# add the regression line
plt.plot(df["gEUR"], intercept + slope * df["gEUR"])
plt.legend(handles=labels)
plt.xlabel(xlab1)
plt.ylabel(ylab1)
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

# the "with" command allows us to maintain a certain style only for a certain block of code
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
    # we can also add manual placed text boxes on our plot:
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
    # we can save the plot as png
    plt.savefig("Plots/plot1.png")
    # and also as other formats such as pdf
    plt.savefig("Plots/plot1.pdf")



# Regressions -------------------------------------------------------------


# as mentioned above: we can use regression analysis to extract useful information from our data
df = df_original[["gEUR","Exp_All_R"]]
df = df.dropna(axis = 0, how = "any")
reg1 = scipy.stats.linregress(df["gEUR"], df["Exp_All_R"])

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

  

  
  
  
  
  
  
  
  
  
