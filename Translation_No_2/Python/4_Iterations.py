#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 14:07:51 2017

@author: dominiquepaul
"""
# Packages -----------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Description -----------------------------------------------------

# Machine learning is based on repeating small "learning steps"
# over and over again. We will need a programming structure that
# allows us to do this in an efficient way.

# You have already seen the function sapply that does something similar. 
# But for machine learning, we often want a more transparent way to do 
# iterative steps. In fact we use "loops". 
# Specifically, "for-loops" and "while-loops". In this script, we
# consider how they work

# A for-loop --------------------------------------------------------

# We want to check whether the mean of repeated simulated draws 
# from a normal distribution with a given mean really converges
# to that mean. (In other words, we check the law of large numbers.)


# Here is how you can simulate data
x = np.random.normal(10, #mu 
                 11, #sigma
                 1) # amount of numbers to be created
# this creates a random number following a normal distribution

# Some parameters that we need
theory_mean = 10
iter_range = np.arange(1,101,1)


# We need an object that collects the single random draws.

# An empty vector that we are going to fill up
# with randomly drawn numbers (in fact, it's not 
# empty but contains zeros).
sample_list = np.zeros(len(iter_range))

# And another vector that we are going to fill up
# with the resulting means:
sample_mean_list = np.zeros(len(iter_range))

# In the jargon, this means preallocating an output object.

# Creating some empty (zero) "containers" that are going to
# be filled up in a loop is called "pre-allocation".
# Make sure to always use this when performing heavy
# calculations. It is much more efficient than 
# making an existing vector longer by one element
# at a time!

# So here is how we may perform the loop
for i in iter_range:
    sample_list[i-1] = np.random.normal(theory_mean, 10, 1)
    sample_mean_list[i-1] = np.average(sample_list[0:i])

x = pd.DataFrame({"iter_range":iter_range,"sample_list":sample_list,"sample_mean_list":sample_mean_list})
x

# Let's do a quick-and-dirty plot 

plt.scatter(x["iter_range"], x["sample_list"], c = "blue", s = 3)
plt.plot(x["iter_range"], x["sample_list"], c = "blue", linewidth = 0.5)
plt.plot(x["iter_range"], x["sample_mean_list"], c = "red", linewidth = 2)
plt.show()


# As you see, plotting helps a lot for getting "a picture" what
# you are actually doing...


# A highly inefficient for-loop -------------------------------------------

# Never do this:

sample_list = 0; sample_mean_list = 0

for i in iter_range:
    a = np.random.normal(10,10,1)
    sample_list = np.append(sample_list, a)
    sample_mean_list = np.append(sample_mean_list, np.average(sample_list))
    
sample_list
sample_mean_list


# This works fine as long as you run easy stuff. But
# it is extremely inefficient in terms of the inner
# "physical logistics" of the computing process!



# A while loop ------------------------------------------------------------

# Now suppose that we want something different. 
# Not a fixed iterRange, but repeat until 
# a certain condition is met, say the red curve from before
# (the sample mean) does not change any more. In mathematical
# terms, we put a "convergence condition".

# This needs an additional step. We need an 
# initial situation and check whether the condition 
# already holds initially.

# Let's set a maximum number of "iterations", to prevent
# our program for running forever if 
imax = 100000

# We do not know how many iterations we will actually run,
# so we set our empty containers to a length of imax
sample_list = np.zeros(imax)
sample_mean_list = np.zeros(imax)
crit_list = np.zeros(imax)
theory_mean_list = np.repeat(theory_mean, imax)


i = 0 # set at zero as indexing starts at 0 in python 

crit = 1000  # critical value for passing test whether
             # more iterations should be run.
             # Initialize crit at a high number that
             # certainly does not meet the condition

tolx = 1e-6  # if crit meets this value, the loop stops


while crit > tolx and i <= imax:
    sample_list[i] = np.random.normal(theory_mean, 10, 1)
    sample_mean_list[i] = np.average(sample_list[:i+1])
    
    # For the first draw (i=1), there is no "previous" draw.
    # So keep crit at the initial value

    if i > 1:
        crit = abs(sample_mean_list[i] - sample_mean_list[i-1])  / abs(sample_mean_list[i-1])

    # What does crit actually measure?
    # Does this remind you of some mathematics?
  
    crit_list[i] = crit 
    
    i = i + 1


# In mathemaical terms, the idea is (somewhat loosely speaking):
# we hope to have a Cauchy sequence, which implies that it converges
# Ask google if you are interested :-)

# Collect the entire output of interest in a dataframe.
# Note that name that is provided to the first column.

y = pd.DataFrame({'id': range(imax), 'theory_mean_list': theory_mean_list, 'sample_list': sample_list, 'sample_mean_list': sample_mean_list, 'crit_list': crit_list})

# Y still contains many zeros. In fact, from the row 
# corresponding to the current 
# value of i on, nothing has been filled. 
# Let's cut Y at that row
y = y.iloc[0:i,:]

# inspect the last few rows of Y.
# What can you infer?
y.tail(10)


xlab1 = "Draw(s)"; ylab1 = "Value"


# What does this graph show?
# What does the alpha do?
plt.plot(y["id"],y["sample_mean_list"], c = "red", linewidth = 1.2)
plt.plot(y["id"],y["theory_mean_list"], c = "black", linewidth = 2)
plt.xlabel(xlab1)
plt.ylabel(ylab1)
plt.title("The mean approaches its theoretical value")



# Only the last N observations to study convergence in detail
N = 100

plt.plot(y["id"][-N:],y["sample_mean_list"][-N:], c = "red", linewidth = 1.2)
plt.plot(y["id"][-N:],y["theory_mean_list"][-N:], c = "black", linewidth = 2)
plt.xlabel(xlab1)
plt.ylabel(ylab1)
plt.title("The mean approaches its theoretical value")


# The types of graphs we have here are useful for machine learning.
# There is one catch. So far, it is not easy to create nice legends
# that tell you which line represents what. In the next section
# we look at an elegant way to produce high-quality graphs.


# Sophisticated graphs with informative legends -------------------------------


# Often the best way to proceed is to bring the data into
# the long format (yes, in the untidy long format...)

# This allows for creating labels for legends etc. You can achieve almost
# everything in this way. 
# Below, we just look at a few examples.

# To get from wide to long, you need the opposite of spread(), 
# which is gather(). Since everything is a bit complex, 
# we first use toy data to work with.


toy = y.iloc[0:5, 1:5]
# What did we do here?
# You can read about subsetting in the book on pp. 300-302.


toy.columns
# The wide-to-long process is somewhat tricky.
# The first argument specifies the columns that
# are going to be stacked on top of each other.
# The respective column names go into the new "key" column.
# (You notice that it is really the reverse of spread()!)
# We call the key column "series". The values in the new long format
# will be in a column with name "Value".

to_plot = pd.melt(toy, # the data
                  id_vars=['id'], # the values which serve as identification 
                  value_vars= ['theory_mean_list', 'sample_list', 'sample_mean_list']) 
                 # the values which we want to stack


# The simplest thing we can plot is this:
groups = to_plot.groupby('variable')
for name, group in groups:
    plt.plot(group.id, group.value, label = name)
    plt.legend()
plt.show()



# This looks very ugly, but there is an informative legend,
# something we did not have before!

# Of course, we want the legend to show telling names.
# As we have done before, we create nice telling labels with sapply:

# Inspect the values in the series column...
to_plot["variable"].unique()

# By now, you know how this works!
to_plot["Legend"] = to_plot["variable"]
to_plot["Legend"].replace(["sample_list","sample_mean_list","theory_mean_list"],["Single draw","Sample mean","Theor. mean"], inplace = True)

# Now, we can use the color asthetic for creating an appropriate legend
# The simplest thing we can plot is this:
groups = to_plot.groupby('Legend')
for name, group in groups:
    plt.plot(group.id, group.value, label = name)
plt.legend()
plt.show()

# or with legend title
for name, group in groups:
    plt.plot(group.id, group.value, label = name)
plt.legend(title= "Legend")
plt.show()


# We still want to make this look nicer, by pickig colors manually
# and selecting specific linetypes.
# Let's look at this with only two series

to_plot["Legend"].unique()

# Select only the columns that we are interested in
to_plot2 = to_plot.loc[to_plot["Legend"] != "Single draw",:]

groups = to_plot2.groupby('Legend')
for name, group in groups:
    plt.plot(group.id, group.value, label = name)
plt.legend()
plt.show()

# add Line type
# In the R script we let the program choose randomly based on a string
# this is not possible with mpl
# but we can easily just define a dictionary with line types depending on 
# the name which we can call every time:
line_dict = {"Sample mean": "-", "Theor. mean": "-."}

for name, group in groups:
    plt.plot(group.id, group.value, label = name, linestyle = line_dict[name])
plt.legend()
plt.show()

# we can do the same for colors; lets add a manually chosen color scheme:
color_dict = {"Sample mean": "red", "Theor. mean": "black"}

for name, group in groups:
    plt.plot(group.id, group.value, label = name, color = color_dict[name])
plt.legend()
plt.show()

# Manual color and linetype scheme
for name, group in groups:
    plt.plot(group.id, group.value, label = name, linestyle = line_dict[name], color = color_dict[name])
plt.legend()
plt.show()


# And with a "size" scheme...
size_dict = {"Sample mean": 1, "Theor. mean": 0.5}
for name, group in groups:
    plt.plot(group.id, group.value, label = name, linestyle = line_dict[name],
             color = color_dict[name], lw = size_dict[name])
plt.legend()
plt.show()

# Now that we have played around with the toy data of just the first five
# rows of Y, we can proceed to plot the entire sample.



# A fully-fledge graph ----------------------------------------------------


# In complete analogy to the toy version above

to_plot = pd.melt(y,id_vars=['id'], value_vars= ['theory_mean_list', 'sample_list', 'sample_mean_list']) 

to_plot["Legend"] = to_plot["variable"]
to_plot["Legend"].replace(["sample_list","sample_mean_list","theory_mean_list"],["Single draw","Sample mean","Theor. mean"], inplace = True)


to_plot2 = to_plot.loc[to_plot["Legend"] != "Single draw",:]

# we create one bigger dicitonary with two sub dictionaroes as elements to make things easier
plot_dict = {"Sample mean": {"linetype":"-","color":"red","lw-size":1},
          "Theor. mean": {"linetype":"-.","color":"black","lw-size":0.5}}


# Sample mean and theoretical mean
with plt.style.context(('ggplot')):
    groups = to_plot2.groupby('Legend')
    for name, group in groups:
        plt.plot(group.id, group.value, label = name, linestyle = plot_dict[name]["linetype"],
                 color = plot_dict[name]["color"], lw = plot_dict[name]["lw-size"])
    plt.xlabel("Draw(s)")
    plt.ylabel("Value")
    plt.title("The mean of a sample approaches its theoretical value")
    plt.legend()
    plt.show()


# With only a limited range in the x and y direction 
# (for closer inspection)
with plt.style.context(('ggplot')):
    groups = to_plot2.groupby('Legend')
    for name, group in groups:
        plt.plot(group.id, group.value, label = name, linestyle = plot_dict[name]["linetype"],
                 color = plot_dict[name]["color"], lw = plot_dict[name]["lw-size"])
    plt.xlabel("Draw(s)")
    plt.ylabel("Value")
    plt.title("The mean of a sample approaches its theoretical value")
    plt.legend()
    # add xlim and ylim
    plt.xlim([500, max(to_plot2["id"])])
    plt.ylim([9, 11])
    plt.show()

# Including the sample draws...

# lets add another element to the dictionary first
plot_dict = {"Sample mean": {"linetype":"-","color":"red","lw-size":1},
          "Theor. mean": {"linetype":"-.","color":"black","lw-size":0.5},
          "Single draw": {"linetype":"--","color":"grey","lw-size":0.5}}


# You don't see much here...
with plt.style.context(('ggplot')):
    groups = to_plot.groupby('Legend')
    for name, group in groups:
        plt.plot(group.id, group.value, label = name, linestyle = plot_dict[name]["linetype"],
                 color = plot_dict[name]["color"], lw = plot_dict[name]["lw-size"])
    plt.xlabel("Draw(s)")
    plt.ylabel("Value")
    plt.title("The mean of a sample approaches its theoretical value")
    plt.legend()
    plt.show()



# lets include alpha (opacity) and change line sizes to improve some visibility
plot_dict = {"Sample mean": {"linetype":"-","color":"red","lw-size":2,"alpha":1},
          "Theor. mean": {"linetype":"--","color":"black","lw-size":2,"alpha":1},
          "Single draw": {"linetype":"-","color":"grey","lw-size":0.5,"alpha":0.5}}


with plt.style.context(('ggplot')):
    groups = to_plot.groupby('Legend')
    for name, group in groups:
        plt.plot(group.id, group.value, label = name, linestyle = plot_dict[name]["linetype"],
                 color = plot_dict[name]["color"], lw = plot_dict[name]["lw-size"], 
                 alpha = plot_dict[name]["alpha"])
    plt.xlabel("Draw(s)")
    plt.ylabel("Value")
    plt.title("The mean of a sample approaches its theoretical value")
    plt.legend()
    plt.show()




 



