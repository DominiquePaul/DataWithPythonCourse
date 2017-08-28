#################
# Lecture 2 live
#################

# Topics of this lecture
# 1) Juggling with dataframes
# 2) Reading data from a website
# 3) Package
# 4) Loops
# 5) Drawing random numbers from a particular


# we again first of all import all our packages which we are going to need
import pandas as pd
import numpy as np
import sys
import os

# set our directory where we will get our files from and save new ones to
os.chdir("/Users/dominiquepaul/xJob/1-DataWithPythonCourse")

# we can also read in data from websites
shop_list_0 = pd.read_html("http://www.einkaufszettel.de/einkaufslisten/einkaufszettel-vorlage")

# This is a list
print(type(shop_list_0))
print(len(shop_list_0))
# in it there are various data frames
print(type(shop_list_0[1]))

# Select second list item
shop_list = shop_list_0[1]
print(type(shop_list))


########################################
# Selecting items from a data frame
########################################

# similar to R, we can grab items from a df via their position
# however, different than in R, items are indexed starting with 0
# so if you want to get the first row or column, you have to use '0' 

# we select the second row and all columns here
# even if we are not selecting a row or column, we have to use ':' as a placeholder 
# as the function wont work otherwise

test1 = shop_list.ix[1,  #rows
 :] #columns
#we could use squared brackets after our selection of the row/column to select the n-th item of our selection if relevant

# selecting all rows and the second column
test2 = shop_list.ix[:,1]
print(type(test2))

# selecting the first item from all rows and the second column 
test3 = shop_list.ix[:,1][0]
print(test3)

# selecting the first two rows of the data frame and all rows
test4 = shop_list.ix[0:2,:]
print(test4.head())

# note that the notation is start:stop, thus we start with row number 0,
# but we stop BEFORE row 3 (which is 2 in the index). We thus get rows 0 and 1

# deleting rows and columns from the list:
shop_list1 = shop_list.drop(0, # indicates the row or column to be dropped (remember indexing begins with 0 )
	axis = 0) # axis indicates whether we want to drop a row or column (0 = row, 1 = column)
print(shop_list1.head(2))

# dropping multiple rows at the same time
shop_list = shop_list.drop([0,2], axis = 0)
print(shop_list.head(2))

# creating an array with the columns we want to select
sequence = np.linspace(0, #starting point
	8, # ending point
	5) # amount of evenly spaced numbers to be created
print(sequence)

# we only select the columns which are names
shop_list1 = shop_list.ix[:,sequence]

# lets delete all 'test' variables as we dont need them anymore 
# and in order to avoid later confusion
# dir() gives us a list of all variables existing in python
# via the for loop we can iterate through all of then and check whether
# the begin with test, if so we delete them
for name in dir():
    if name.startswith('test'):
        del globals()[name]

# Tests for getting all shopping items in one column
test1 = pd.concat([shop_list.ix[:,0],
	shop_list.ix[:,2],
	shop_list.ix[:,4], 
	shop_list.ix[:,6],
	shop_list.ix[:,8]])

# convert the file from a series to a dataframe
test1 = pd.DataFrame(test1)

# initialize an empty series (similar to array)
test2 = pd.Series([])

# range creates an array from 0 to the amount of columns through which we can iterate
for i in range(0, len(shop_list.columns)):
	# this combines the two elements to one
	test2 = pd.concat([test2, shop_list.ix[:,i]])

test2 = pd.DataFrame(test2)

shop_list = test2
print(type(shop_list))
print(shop_list)


# we see that the index is not constant, lets change this: 
# resets the index, this would push in the old one as a columns so we delete it with the drop command
shop_list.reset_index(drop = True, # by resetting the index the 'old index' would be pushed in as a new index, this command stops this from happening
 inplace = True) # allows the command to be used on the df itself, otherwise we would have to use df = df.reset_index(...)

# change column name
shop_list.columns = ["item"]
print(shop_list)


# as we see not all items are strings though
print(type(shop_list.item[12]))
# or by looking at 
dtypeCount = shop_list.item.apply(type).value_counts()
print(dtypeCount)

# lets change this
shop_list['item'] = shop_list['item'].astype('str') 

###################################################
# printing our output to a seperate text file
###################################################

# save old system output (the place where python directs its output) 
# so we can change back later if we wish
orig_stdout = sys.stdout
# create file where we want to save the output
file = open('inspectWhatWeAreDoing.txt', 'w')
# change output to normal 
sys.stdout = file

# compares to see which rows are empty
print(shop_list.ix[:,'item'] == "nan")

# prints the row numbers where the rows are empty
print(shop_list.loc[shop_list['item'] == "nan"].index.tolist())

# revert output to original location
sys.stdout = orig_stdout
# save file
file.close()


# Now we still want to drop the empty rows from shopList

list_to_delete = shop_list.loc[shop_list['item'] == "nan"].index.tolist()
shop_list1 = shop_list.drop(list_to_delete, axis = 0)

print(shop_list1)
