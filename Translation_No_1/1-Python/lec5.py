#############################################
# LECTURE 5: Handling data and data.frames #
#############################################
# We will continute working with the data sets for the SNB
# That you downloaded for Lecture 4.
# This time, we are assuming that the data already look neat
# So no deletion of empty columns any more.
# Preparatory steps
###################
# Almost everytime you work with data, you should do the
# following steps...
import os
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
import statsmodels.formula.api as smf


# set working directory 
os.chdir("/Users/dominiquepaul/xJob/1-DataWithPythonCourse/4-Data/")

rawXrates = pd.read_csv('dataXrates.csv', sep = ",")


# Referring to columns in data.frames
#####################################
# There are (at least) two ways to refer to a column:
# rawXrates[["D0"]]
# rawXrates.D0.head
# For instance, you can use this for getting all the values in a column

print(len(rawXrates.D0.unique()))
print(rawXrates.D0.value_counts())

# Note the subtle difference between
print(type(rawXrates[["D0"]]))
print(type(rawXrates["D0"]))
# Sometimes, this matters, sometimes not...
# For deleting empty columns, it does not.

# NOTE: Our data is in the so-called "long" format: all variables (in the statistical
# sense) are "stacked".
# The statistical variable names are a combination of D0 and D1.
# The SNB does not make it too easy to get the meaning of D0. But if you go
# to the Data Portal https://data.snb.ch/de/topics/ziredev#!/cube/devkum
# and download the data in Excel format (which can also be read into pandas
# using the command: pandas.read_excel), you get the meaning of the exchange rates.

# Converting data from "long" to "wide" and back to "long"
##########################################################

print(rawXrates.head())

long_prep_df = rawXrates.copy()
long_prep_df['join'] = long_prep_df["D0"] + '_' + long_prep_df["D1"]

print(long_prep_df.head())
wide = long_prep_df.pivot(index='Date',columns='join', values='Value')
wide = wide.reset_index()
print(wide.tail())




# convert back from wide to long
long1 = pd.melt(wide, # data frame to be used
	id_vars='Date') # the 'id' variable which we want to keep in each row
# we could also add the variable value_vars='' in 
# case we only want to keep of the other rows

print(long1.tail())
# D0 and D1 are now merged, we could change this but we'll focus on other things for now

# we create a new time identification which we can use for time series purposes
# .str[startAt:endBefore] slices the column into a part, remember that string indexing in 
# python starts at 0. The slicing will stop BEFORE the ending index. Try this out on an own
# string to get a feel for it
# .astype(int) converts the column from string to integer
rawXrates['year'] = rawXrates.Date.str[0:4].astype(int)
rawXrates['month'] = rawXrates.Date.str[5:7].astype(int)
rawXrates['timeId'] = rawXrates.year + (rawXrates.month -1) / 12

print(rawXrates)


# Eliminating rows and columns from data.frames
# (= selection of subsets of data)
################################################
# Let's get rid of all data before 2000

xrates = rawXrates.copy()
xrates = xrates.ix[xrates['timeId'] >= 2000]
print(xrates.head())
# Now you can see why we needed the dates in numerical format
# Next we get rid of other information we are not interested in

print(xrates.D0.value_counts())
xrates = xrates.ix[xrates['D0'] == 'M0']
print(xrates.head())

print(xrates.D1.value_counts())
xrates = xrates.ix[xrates['D1'] == 'EUR1']
print(xrates.head())

#plt.plot(xrates.timeId, xrates.Value)
plt.show()

# we can also change parameters of our graph
#plt.plot(xrates.timeId, xrates.Value, 'r--', linewidth=0.5)
plt.show()

print(xrates.head())

# we can also subset the data using the .query method. 
# We then select our columnsm, which we want to keep after filtering
xrates_alt = rawXrates.query('year >= 2000 and D0 == "M0" and D1 == "EUR1"')[['timeId', 'D1','Value']]

print(xrates_alt.head())

# lets delete the variables we dont need any more
del  long1, wide, long_prep_df, xrates_alt


# Analyze the correlation between the USD and EUR exchange rate
###############################################################
# print(rawXrates.head())

data = rawXrates.query('(D1 == "EUR1" or D1 == "USD1") and D0 == "M0" and timeId >= 2000')[['timeId','D1','Value']]
data = data.pivot(index='timeId' , columns='D1').reset_index()
data.columns = ["timeId", "EUR1", "USD1"]
print(data.head())

# plot both linews against each other
plt.plot(data.timeId, data.EUR1, "r",data.timeId, data.USD1, "b")

# or consequtively (uncomment yourself)
# plt.plot(data.timeId, data.USD1, "r")
# plt.plot(data.timeId, data.USD1, "b")

plt.title('Wechselkurse € und $')
plt.xlabel("Time")
plt.ylabel("EUR, USD")
plt.grid()
plt.legend(["EUR","USD"])  
plt.show()

# correlation
corr1 = scipy.stats.pearsonr(data.EUR1, data.USD1)
# this returns us the correlation value as well as the two-tailed p-value
# we are only interested in the correlation
print("the correlation is " + str(corr1[0]))

# regression
reg1 = scipy.stats.linregress(data.EUR1, data.USD1)
# we get an object with containg multiple attributes regarding our regression analysis
# we can either print out everything at once
print(reg1)
# or access single attributes on their own (e.g. for further computation)
print(reg1.pvalue)

# # Another (prettier option) is the statsmodels package
# results = smf.OLS(data.EUR1, data.USD1).fit()
# # Inspect the results
# print(results.summary())

