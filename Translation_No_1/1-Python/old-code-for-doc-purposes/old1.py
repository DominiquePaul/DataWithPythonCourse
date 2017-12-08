


# when trying to create a vector in python, we can proceed the same as in r
list1 = [1,3,4]

# however, taking a closer look we see that this is not actually a vector but a list
print(list1[1])

# this is because vectors/arrays dont exist per se in python
# an vector / array has the same data type, lists can contain multiple data types, so this works:
list2 = [5, True, "hello"]

# to find out more about the differences between lists and arrays, as well as their differences, go to:
# https://stackoverflow.com/questions/7496251/what-is-the-advantage-of-linked-list-over-an-array-and-vice-versa

# using arrays is generally more efficient in data analysis as long as we do not want to
# insert new values in the middle of an array

# so how can we use vectors / arrays in python?
import numpy as np

# we use packages such as Numerical Python (numpy)
# packages are prewritten code and tools which we can just 'copy' for our use
# as python is a multi-purpose language and therefore not made explicitly for data analysis
# we will frequently rely on packages

# we declare the array:
array1 = np.array([42,7,21])

#arrays are indexed starting at 0, so if you want to access '42' of the array, you use
print(array1[0])

# when checking the type data structure, we get...
print(type(array1))
#this is the same as a regular array, despite the initially confusing term

# note for students with programming: we could also use a pandas series, but np.arrays are faster
# and as we want to prepare for bigger chunks of data we will therefore choose the faster method
# https://penandpants.com/2014/09/05/performance-of-pandas-series-vs-numpy-arrays/

#so lets say we have the following three arrays
shopList = np.array(["milk (l)", "cereals (packs)","quollfrisch (packs)"])
quantList = np.array([3, 2, 5])
priceList = np.array([1.95, 2.05, 11.95])

# and want to combine them to a combined table, aka a data frame
# we therefore first do all import the pandas data frame
import pandas as pd

# there are two ways to create the data frame
# the faster way
df1 = pd.DataFrame([shopList, quantList, priceList])

# and the nicer way
df2 = pd.DataFrame({'item': shopList,'quantity': quantList, 'price': priceList}, columns = ['item', 'quantity', 'price'])

# when looking at both data frames we see the differences
print(df1)
print(df2)

# notice that the data frames are transposed versions of the other version

# so lets add a new column  
df2['expPerItem'] = df2['quantity'] * df2['price']
print(df2)

# we export our new data frame as a .txt file
np.savetxt(
	# this is the location of our files
	r'/Users/dominiquepaul/xJob/3-DataWithPythonCourse/allscripts/ourdata.txt', 
	# this determines what we want to save
	df2.values, 
	# this is the format of our data
	fmt='%5s', 
	# header is the first line written in the new file, to match it to the columns we use a delimiter
	delimiter="\t", 
	header="item\tquantity\tprice\texpPerItem")

# however, easing future use we may save our dataframe as a csv:
df2.to_csv("/Users/dominiquepaul/xJob/3-DataWithPythonCourse/allscripts/ourdata.csv")








# Maybe you are  familiar with the concept of passing a variable "by reference" and "by value" in R
# Python usually just passes variables by value
# If you want to find out more about the difference, check this out: 
# https://stackoverflow.com/questions/373419/whats-the-difference-between-passing-by-reference-vs-passing-by-value
