########################################
# LECTURE 4, Part 2: Reading data from #
# csv files and and manipulating them  #
########################################

# as mentioned before Python is a general purpose language and therefore we often have to access packages
# when doing certain things

# to access our working directory we for example have to imoport the os package,
# we do this via the import command followed by the package name
import os
# you already know this one
import pandas as pd
# we are going to need this to be able to plot data later
import matplotlib.pyplot as plt

# Set the working directory to the folder
# where you have the csv files from the SNB

os.chdir("/Users/dominiquepaul/xJob/1-DataWithPythonCourse/4-Data/")
# change this to your directory!!!
# os.chdir("YOUR DIRECTORY")

# Note the forward slashes in the directory!

# On a Mac it may look like this
# os.chdir("/Users/Thomas/Dropbox/Programmierkurs/Data")
# On Windows it may look like this
# os.chdir("D:/Programmierkurs/Data")

# lets load our csv file
# depending on how your data is saved, you might have to use a semi colon or something else a separator
rawXrates = pd.read_csv('dataXrates.csv', sep = ",")

print(rawXrates)


# to infer the type of object we can use type()
# because data frames are not an own object in python, the name of the object which will
# be returned is a so called pandas (the package we are using) data frame
print(type(rawXrates))

# Get the names of the columns ("variables"
# in the statistical sense)
print(list(rawXrates))
# or 
print(rawXrates.columns)

# You can use the names to get a column
print(rawXrates["Date"])

# to print only the first x rows we can use the head function (in this case the first 10)
print(rawXrates["Date"].head(10))
# we can also look at the last x rows by using the tail function
print(rawXrates.tail(5))

# Use this trick to select only the variables you are interested in
varList = ["Date", "D0", "D1", "Value"]

xRates = rawXrates[varList]

print(xRates["Date"].head(10))

# So we got rid of the empty columns!
# lets save the new data as a csv to access later

xRates.to_csv('nameOfNewCSV.csv')

# lets say we dont need a variable in our program any longer
# we can delete it with the 'del command

del rawXrates

# The data looks really enormously big
# Let's say we only care about data from 2010 on
# to start with...

# The next lines of code are preparations for
# data from 2010 on (or any other year)
# We are going to add two new columns to identify the date in a better way

# normally, to slice a string in python we can use use corner brackets after the string to extract a part
# e.g. "hello world"[0:4] will become "hell"
# you can experiment with the following line:
# print("hello world"[0:4])

# however, since we are using the pandas package we wont be able to do this as we would simply
# extract the first x elements by adding [0:x] to the end of our selection as in the following line:
# this would be wrong  xRates["year"] = xRates["Date"][0:4]

# instead we use the .str[0:x] command to extract the substrings while filtering
# xRates["year"] = int(xRates["Date"].str[0:4])

# to turn this into a integer at the same time while slicing the column, we add the
# command pd.to_numeric()

xRates["year"] = pd.to_numeric(xRates["Date"].str[0:4])
xRates["month"] = pd.to_numeric(xRates["Date"].str[5:7])


# a unique identifier for time
xRates["timeID"] = xRates.year + (xRates.month -1) / 12

xRates = xRates.loc[xRates["year"] >= 2010, :]

# Next we get rid of other information we are not interested in...

xRates["D0"].unique()

xRates = xRates.loc[xRates["D0"] == "M0"]


# And we select data on just the EUR exchange rate

xRates["D1"].unique()
xRates = xRates.loc[xRates["D1"] == "EUR1"]



# plotting
# before we start plotting we have to conver the value column from a string to an integer
xRates["Value"] = pd.to_numeric(xRates["Value"])
print(type(xRates.iloc[1, 3]))



# the r in the end indicates the color (and can also convey the type of symbols / display options used
plt.plot(xRates.iloc[:, 6], xRates.iloc[:, 3], "r")

# if you are executing this script in your terminal you will need the following line 
# if you are using a program such as spyder you can omit the following line
plt.show()
