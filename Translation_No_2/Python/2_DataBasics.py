# Description -------------------------------------------------------------

# In this script, we study how to read data from external sources into Python.
# We then learn how to "tidy up" that data and combine it with other data.
# This means quite a bit of selecting and filtering and juggling with
# rows and columns.


# Getting SNB data on exchange rates -------------------------------------------------------

# To start, go to the data portal of the Swiss National Bank.
# Make Sure to switch to ENGLISH!
# Choose table selection and then foreign exchange market.
# Choose data from January 2001 to present, in csv format.


# Create a folder "Data" within the directory where you run your 
# Pythom´ project for this part of the course ("Data Science Fun/Programming").
# Put the csv file into that folder.
# The file name will be something like snb-data-devkum-en-selection-20170901_1430.csv
# Make sure to get the English version!

# Open the csv file first with Excel.
# In my case it looks pretty ugly. 
# This is because my regional settings misinterpret the data formats.

# Now open the data with a text editor.
# Try to understand how this data is organized.


# Good idea to always first clear all data that are 
# still in the working space to start with a clean sheet:
#%reset

# Packages ------------------------------------------------------------------

import pandas as pd 
import os
from ggplot import aes, ggplot, geom_point, geom_line 
import matplotlib.pyplot as plt


# Assignment: Read SNB data --------------------------------------------------------------


# YOUR TURN: Read the beginning of Ch. 8 (print) and try to get the data into R



# Reading data into R ----------------------------------------------------------------

# change this to your directory
os.chdir("/Users/dominiquepaul/xJob/DataWithPythonCourse1/Translation_No_2/")

# Discussion and solution of above

# First idea to read data:
pd.read_csv("snb-data-devkum-en-selection-20171002_1430.csv")

# Second idea:
pd.read_csv("Data/snb-data-devkum-en-selection-20171002_1430.csv")

# Third idea:
pd.read_csv("Data/snb-data-devkum-en-selection-20171002_1430.csv",sep=";", skiprows=3)

# the argument skiprows refers to the number of rows that are not read into Python.
# Check why this is important!

x_rates0 = pd.read_csv("Data/snb-data-devkum-en-selection-20171002_1430.csv",sep=";", skiprows=3)

type(x_rates0)

# alternative
test = pd.read_table("Data/snb-data-devkum-en-selection-20171002_1430.csv",sep=";", skiprows=3)

# delete variable from environment
del(test)


# Assignment: Read more data ----------------------------------------

# Use google to find the OECD data platform.
# Play around with the platform and try to understand how it works.
# Download some data that you find interesting.

# SOLUTION

# The data portal is at http://stats.oecd.org/. 
# I selected data on Production and Sales (MEI). I got the data set
# MEI_REAL_29102017172534360.csv.

# In my case, it is comma-separated, there is a column header, but no lines to skip.
# oecd = pd.read_csv("Data/MEI_REAL_29102017172534360.csv")


# Selecting rows and columns in a data frame -----------------------------------------------------------

# We go back to the SNB data on exchange rates. Have a look at the data.

# We want to select only Euro and USD, get rid of all the other exchanges rates.
# Then we want to bring the data into a "tidy" format.

# Read about manipulating and tidying tibbles/dataframes
# in the book Chapters 3 and 9.

# We have already carried out some important steps with 
# the shopping list in 1_IntroCoding. But there is more to learn!
# You can read about manipulation of dataframes in Chapters 3 and 9.
# But it's a bit complicated, so we first do some important steps together.



# What columns do we have in our dataframe?
x_rates0.columns

x_rates0["D0"].unique()

# another option is
set(x_rates0["D0"])
# a set is like a list, but unordered and withour replications

# pandas data frames are made up individual (pandas) series, another data type


# D0 is a very boring column that does not contain valuable
# info (it means that the data contains monthly averages.)
# So we just drop it...

# Drop D0
x_rates = x_rates0.drop("D0", axis = 1)

# or:
#x_rates = x_rates0.loc[:, x_rates0.columns != "D0"]

# What values are in D1?
x_rates["D1"].unique()

# What is an alternative way to inspect what 
# values we have in D1?



# Now we want to get rid of most of the rows.
# We choose to work only with the rows that belong 
# to EUR and USD observations (the 1 in EUR1 etc. means
# that the exchange rate is *1* EUR per 1 CHF).

# the command compares whether each row value for the D1 column
# is matches our list representing the dollar and the euro. If so, it is 
# copied, if not then it is skipped

# the .isin(values) method checks whether the column values match the one of the values
# in our list of possible values

# or alternatively:
xrates = x_rates.query('D1 == ["USD1", "EUR1"]')


# From long to wide -------------------------------

# In a tidy data frame, columns represent "variables" in the 
# statistical (rather than programming) sense.
# Recap: What is a statistical variable?
# What is a variable in programming?


# Our data is NOT tidy! One single column
# mixes quite some info that we have a separate interest
# in: We are SEPARATELY interested in EUR and USD exchange
# rates, we do not want them "stacked" on top of each other.

# Rather, we want to have separate columns for EUR and USD
# and this means the data will get "wider" and only half as 
# "long." Let's see how we get there (a bit tricky).

x_rates_wide = x_rates.pivot(index='Date', columns = "D1", values='Value')

# The key argument is the column that contains the "labels"/names
# for the new columns that are going to represent *statistical*
# variables. Here, column D1 contains EUR1 and USD1

# The value argument indicates which column
# contains the values that should enter the 
# respective rows of the new variables. Here, 
# this column is already called "Value" (we already
# got the data with this name from the SNB).


# our date column now longer is a column but serves as an index
# should we prefer the date as a column and not as an index we can instead call:

x_rates_wide = x_rates.pivot(index='Date', columns = "D1", values='Value').reset_index()
# which pushes our index into the df



# Strings, numeric date format ---------------------------------------

# Read about strings in Ch 11.

type(x_rates_wide.loc[:,"Date"][0])
# We have Dates as characters. 

# Since we want to be able to use the
# dates for some numerical calculations, we convert them into 
# numbers. For later use, we want to keep info about years and 
# months separate.

# Use the function mutuate to create a new variable
# (and we continue using the pipe operator)
x_rates_wide["year"] = x_rates_wide["Date"].str[0:4].astype(int)

# the .str allows us to do operations on a big scale with the individual strings in the column "year"
# by using [0:4] we slice each element to extract the 1st until the 4th element (remember the index starts at 0) 
# .astype(int) turns these strings into integers

# So this works as intended.

# Let's do the same with months (YOU do it!)

# The solution is:
x_rates_wide["month"] = x_rates_wide["Date"].str[5:7].astype(int)

type(x_rates_wide["year"][0])
type(x_rates_wide["month"][0])

# Let's calculate a new column containing 
# date information in a single numerical format

x_rates_wide["date_num"] = x_rates_wide["year"] + (x_rates_wide["month"] - 1) / 12

# Why do we subtract 1 from month??



# A first plot ------------------------------------------------------------

# Note: the best-practice for plotting in python is to use the MatplotLib package
# there also a version of the ggplot library however it is modelled on the R-package
# and thus not ideal for extensive use in python 
# For this lesson we will use both packages to make the differences clear, starting 
# with next script thought we will use ONLY the MatplotLib package

ggplot(x_rates_wide, aes(x='date_num', y='EUR1')) +\
    geom_point()

plt.plot(x_rates_wide["date_num"],  # the x-axis
         x_rates_wide["EUR1"], # the y-axis
         ".") # this indicates that we wont a scaterplot chart
plt.show() # this shows the graph
    


# This works, but sometimes we might have the problem that the data aren't floats yet
# If necessary we can change this via:

x_rates_wide["EUR1"] = x_rates_wide[["EUR1"]].astype(float)
x_rates_wide["USD1"] = x_rates_wide[["USD1"]].astype(float)

# Note: Double is the most precise
# numeric format (and integer is the least
# precise). Double makes sense for a variable
# like exchange rates. You can read more about
# the double format on p. 294 of the book.

plt.plot(x_rates_wide["date_num"], x_rates_wide["EUR1"], ".") 
plt.show() 

# It's maybe more fun and interesting to plot
# the two exchange rates at once. For this, we 
# use geom_line()

# Note: we are omitting "data = " and "x = "
# It still works.
ggplot(aes(x='date_num'), x_rates_wide, ) +\
    geom_line(aes(y='EUR1')) +\
    geom_line(aes(y='USD1'))
    
plt.plot(x_rates_wide["date_num"], x_rates_wide["EUR1"], "-k", # "-" means line, "k" means black
         x_rates_wide["date_num"], x_rates_wide["USD1"], "-k") 
plt.show() 
# check out the matplotliub documentation for more info on the types of line-types
# and colours you can use:
# http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.plot
    
    
# This looks a little boring. Let's make it more colorful
ggplot(aes(x='date_num'), x_rates_wide, ) +\
    geom_line(aes(y='EUR1', color = "red")) +\
    geom_line(aes(y='USD1', color = "green"))

# alternative ways of setting colors in matplotlib
plt.plot(x_rates_wide["date_num"], x_rates_wide["EUR1"], "-", color = "chartreuse") # this is a html colour
plt.plot(x_rates_wide["date_num"], x_rates_wide["USD1"], "-", color = "#FFA500") # this is a hex colour
plt.show() 

# We will explore plotting im more depth in 3_plotting.R.


# Getting data on exports -----------------------------------------

# We want to analyze the relationship between exports and exchange rates
# Go again to the data portal of the SNB, choose "Economic Data" and 
# "Foreign trade by goods category". Make sure to download data from the 
# English site, so we all get the same data. Choose again data from Jan 2001
# until present in csv format. Download the data and put them again in the 
# same data folder. In my case, the file is called snb-data-ausshawarm-en-selection-20170921_0900.csv.

# Read
trade0 = pd.read_csv("data/snb-data-ausshawarm-en-selection-20170921_0900.csv", sep = ";", skiprows = 3)

trade0


# Functions --------------------------------------------------------

# We need again transform the date info into a numeric format as above.
# Suppose we want to download even more data sets where we need to 
# make this same calculations. It would be quite silly to every time
# do this with copy/pasting the respective code. Why?

# The programming structure that allows you to get a lot more efficiency
# is a FUNCTION. It's a flexible template of code that you can tweak
# to your specific use with the help of "arguments". 

# so let us use a function to generate a variable with a numeric date info.


# Prepare the construction of a function.
# The arguments in functions need generic names that are
# "place holders" for the names of the variables that you actually want to use.
# It is common to use df as a placeholder for any dataframe
# that you may use as an argument of a function.

# Look at this code: We assign our dataframe 
# trade0 the generic name df. (In a way, that's what
# happens if you pass trade0 as an argument into a function.)
df = trade0

# And we assign a particular column that we are 
# interested in a generic name col.
col = df["Date"]
# We introduced this in the context of lists
# at the end of 1_IntroCoding.

# Now we simply use the code that we developed above:
df["year"] = col.str[0:4].astype(int)
df["month"] = col.str[5:7].astype(int)
df["date_num"] = df["year"] + (df["month"] - 1) / 12


# A function let's us to use the very same code
# as a template for any argument that may 
# take on the role of df. 


def calc_num_date(df, col):
    """Creates a continuous timestamp column in a data frame
    
    Keyword arguments:
    df -- the data frame in which the timestamp should be created
    col -- the column from which the data from the time stamp shall be taken
    """
    # this is how you document functions in python properly, read more here:
    # https://www.python.org/dev/peps/pep-0257/
  
    col = df[col]
  
    df["year"] = col.str[0:4].astype(int)
    df["month"] = col.str[5:7].astype(int)
    df["date_num"] = df["year"].astype(int) + (df["month"].astype(int) - 1) / 12
 
    return(df)
    # In this case, this is not strictly necessary. But
    # You will see below that it sometimes is... It tells
    # the function to "give back" df as the output of the
    # function. Put differently, it means: "please give back the *entire*
    # data frame df, and not just the new column Date (or so).




# So this is our template that we can use
# with any suitable data frame. Let's
# check it out:

trade = calc_num_date(trade0, "Date")
# Inspect the trade dataframe to see what happened.




# Here is an even better way to specify
# this function. We assign the col-argument
# a default value.

def calc_num_date(df, col = "Date"):
  
    col = df[col]
  
    df["year"] = col.str[0:4].astype(int)
    df["month"] = col.str[5:7].astype(int)
    df["date_num"] = df["year"].astype(int) + (df["month"].astype(int) - 1) / 12
 
    return(df)

# throught this we set a default or fallback value for the argument col
# The idea of a default is that it can be
# overwritten if the argument is provided
# explicitly. 

# Check it out: We only need one single argument now:

test_trade = calc_num_date(trade0)

test_xrates = calc_num_date(x_rates0)
# Read more about functions in Chapter 15.

# Delete the test objects
del(test_trade, test_xrates, df, col)




# Assignment: Your first function -----------------------------------------

# Write a function that converts a column of a dataframe into a 
# a double format. (The old column get's replaced and keeps the
# same name.) Apply it to the column "Values" of the trade dataframe.
# Give the function a telling name. Use "Value" as a default argument
# for the column name.

# Hint: First figure out how you change the values of
# a column using the [[]] syntax of data frames. Do not
# use pipes, and do not use mutate()! (With pipes and mutate, the
# problem is more difficult ;-)

# The solution is just one line, wrapped by the function syntax!

# Those with substantial background knowledge can try to do it also with "mutate".

# Here goes my SOLUTION (and the steps to develop it).

type(trade["Value"])

#col = "Value"; df = trade


def col_to_num_dnw(df, col = "Value"):
    df[col] = df[col].astype(float)
    
# DNW stands for "Does Not Work" (as intended) ;-)
    
def col_to_num(df, col = "Value"):
    df[col] = df[col].astype(float)
    return(df)
    
test_col_to_num_dnw = col_to_num_dnw(trade)
test_col_to_num = col_to_num(trade)


# Can you see the difference?
# In the DNW version, the function only returns
# the column that we changed. This behavior is 
# somewhat "buggy", but every language has some
# buggy behavior that is not always easy to anticipate.

# Now let's use the proper function

trade = col_to_num(trade)

type(trade["Value"][0])

# And let's clean up. Let's delete everything that starts with "test"

# Try to google this! I googled
# <"del all variables in python similar to"> and used a modification of the second hit
# https://stackoverflow.com/questions/26545051/is-there-a-way-to-delete-created-variables-functions-etc-from-the-memory-of-th

for var in dir():
    if "test" in var:
        del(globals()[var])

# You can also remove functions
del(col_to_num_dnw)






# Loops via sapply() -----------------------------------------------------

# Now we go on with our trade data set (data on exports).
# Let's try to figure out what type of information we have in there.

# Specifically, let's try to figure out what the letters in the columns mean
trade["D0"].unique()

# Go to the German version of the SNB site where you downloaded the data...
# After some detective work, you may get a clue...

# We want to give these {E, A, H} better names.
# Note that this is a combination of a "conditional" task 
# and a loop. 

# Here is the conditional part. It's a bit like
# If the value is "E", replace it with (say) "Imp".
# If the value is "A", replace it with "Exp". Etc.

# And here is the problem from the loop perspective:
# Loop through all letters in D0. For the first letter, 
# change the value to "Imp", for the second, change it to "Exp" etc.

# It would be quite cumbersome to programm such a thing explicitly.
# So R has some special functions that do it for us.

# The "conditional" part is done by the switch function below.
# the loop is handled by the sapply function.

# Here is the code: 

trade["D0"].replace(["E","A","H"], ["Imp","Exp","TradeBal"], inplace = True)

# the first argumnent defines what shall be replace
# the second argument defines by what the respective value shall be replaced
# as we have multiple arguments we use a list
# finally, the inplace argument tells the computer to modify the original data frame 
# itself instead of just returning a new df

# we could also write:
#trade["D0"] = trade["D0"].replace(["E","A","H"], ["Imp","Exp","TradeBal"], inplace = True)




# Grouping ----------------------------------------------------------------


# Let's turn back to our data and proceed with the other columns

trade["D1"].unique()

# Get the meaning of those values from the 
# Excel version that you can downloaded from the SNB data portal.
# It involves quite some detective work!

# There are, weirdly, two values of TBS, i.e. TBS0 and TBS1
# Let's see, whether there is any important difference:

trade.groupby(["D0","D1"]).size().reset_index()

# the first argument defines the two columns from which unique combinations 
# shall be identified
# .size() counts the number of occurences
# reset index pushes the new index into the df as columns which makes
# reading our result much easier. You can try and see what it looks like without

# What can you infer from this?


# Changing values of trade$D1 ---------------------------------------

trade["D1"].replace(["T", "MAE", "PUB", "C", "TBS0", "F", "M", "U", "P", "TBS1"],
     ["All","Machines","Precision","Chemistry","Clothing","Vehicles","Metals","Watches","Precision (narrow)","Clothing"],
     inplace = True
)


# Finally, let's inspect the D2 column

trade["D2"].unique()

# We could change it with the below code. But
# For the moment we just leave it, so this code is
# out-commented.

#trade["D2"].replace(["WMF","N","R"], 
 #    ["Level (nominal)","Nominal change (in \u0025)", "Real change (in \u0025)"],
  #   inplace = True)

# The reason we do not use this code now is that it would
# be an obstacle below when we change the data from
# long to wide. It would lead to excessively long
# column names.
  
  
# Assignment: Trade data from long to wide --------------------------------------------

# Again, we want to bring the trade data in a format such
# that the info in one column corresponds to a 
# variable in the statistical sense. The goal is to have
# one column for every possible combination of values in 
# the columns D0/D1/D2!

# Take a sheet of paper and try to figure out which combinations
# these are!

# Consider the following possible combinations
trade.groupby(["D0","D1","D2"]).size().reset_index()


# Use this to bring the trade dataframe into a tidy format
# (YOU do it!)

# we create a new column aggregating the names of D0, D1 and D2
trade["key"] = trade["D0"].astype(str) + "_" + trade["D1"].astype(str) + "_" + trade["D2"].astype(str)
# we convert the table from long to wide as we did earlier using the pivot command
trade_wide = trade.pivot(index = "Date", columns = "key", values = "Value").reset_index()
trade_wide = calc_num_date(trade_wide)


# Join tradeWide and xRatesWide --------------------------------------------------

# We want to analyze how exchange rates affect exports.
# For this, it is convenient to have exchange rates and 
# trade data in a single dataframe.

# For this, we use the inner_join() function


d = pd.merge(trade_wide,x_rates_wide, on = ["Date", "year", "month", "date_num"])

# d is a new data frame!
# Let's get rid of the 1 ins USD1 and EUR1
# (Note, these are now column names, no longer
# values in the data frame!)

d.rename(columns = {"EUR1": "EUR", "USD1": "USD"}, inplace = True)


# Changes in Xrates -------------------------------------------------------

# You may have been relieved that, finally, we have all
# the data that we need in one data set, and the data is tidy!
# But there is still a little more work to do.

# When we look at exchange rates and exports, we are often not interested
# in how the level of exchange rates (e.g. 1.60 CHF/EUR) relates to the level
# of exports (e.g. 15 bn CHF). Rather, we want to know how a 
# (percentage) CHANGE in exchange rates is associated with a 
# (percentage) CHANGE in exports.

# For this, we calculate rates of changes. In the
# econ-stat slang, this is often called a "growth rate".

# Pandas has a shift() function. To check what it does consider

d["EUR"].head()
d["EUR"].shift(1).head()
d["EUR"].shift(2).head()
d["EUR"].shift(3).head()


d["gEUR"] = ( d["EUR"] / d["EUR"].shift(1) - 1) *100

# Since we need this more often, let's write a function
# that converts the column of a data frame into growth rates

# YOU DO THIS!

# Here is my solution

def to_growth(df, col_name):
    
    g_rate = ( df[col_name] / d[col_name].shift(1) - 1) *100
    return(g_rate)

# Quiz: If we apply this function to a column in a 
# data frame: 
# 1) How many new columns are created?
# 2) What are the names of these columns

d["test"] = to_growth(d, "EUR")
d["gUSD"] = to_growth(d, "USD")


# remove columns that we do not want
del(d["test"])


# Export/Save -------------------------------------------------------------

d.to_csv("data/TradeEx_tidy.csv")

# or alternatively in a more common method to save a python object
d.to_pickle("data/TradeEx_tidy.pkl")
















