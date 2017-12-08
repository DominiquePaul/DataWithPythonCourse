#script for lecture 1

# Welcome to the course, to start, we are going to explore some basic properties
# of the programming language Python

a = 2
print(a)

# Variables have types. Let's see what's
# the type of a is..

print(type(a))

# are there other types?
a_as_char = "a"
print(a_as_char)

# go on...
b = 3
b_as_whatever = b
print(b_as_whatever)

########################
# algebraic operators
########################

# lets do some algebra
print(a+b)

print(a*b)

# different than in R, we use '**' for exponents, python is not compatible with '^'
print(a**b)

########################
# logicals
########################

# so lets assume that
i = 1
j = i
i = 2

# what will j be? 
print(j)

# to check if i and j are the same, we can use '=='
print (i == j)

# "=" is an assignment operator
# "==" means mathematical equality

# we can save this result in form of
l = i == j
print(l)
print(type(l))

# you can also use '!=' to check if the opposite is true, it has the meaning of 'is not'

# try these and make some modifications of your own to get familiar with the concept
print(True == False)
print(2 == 2)
print(True != False)
print(20 != 10)

# there are more logical operators, try using <, >, >=, <= in the line below
print(10 >= 5)


# there are many more operators, to check them out 
# or find more about operators in general, check out the following link:
# https://www.tutorialspoint.com/python/python_basic_operators.htm


########################
# data structures
########################

# in python (and in programming in general) we use data structures to efficiently store
# data and make further use easy in efficient

# a basic structure for example is a list
shop_list1 = ["milk (l)", "cereals (packs)","quollfrisch (packs)"]
# we can output one element of the list via square brackets
# in python indexing starts at 0, so if you want to extract the first element
# you have to reference it by using 0
print(shop_list1[0])

# lists can contain different data types:
list1 = ["hello", 3, True]

# different than lists is the array, which can only store one data type
# arrays are very useful in data science as they are much more efficient than lists

# there are also more differences and attributes to the both data types which you can find here:
# https://stackoverflow.com/questions/7496251/what-is-the-advantage-of-linked-list-over-an-array-and-vice-versa


# unfortunately however, python is not a data science language its built-in version of the array 
# is not the most efficient for calculations so we will use a array from a package
# packages are prewritten code and tools which we can just 'copy' for our use

# this imports the package and allows us to refer to it later by using 'np'
import numpy as np


# we can declare numpy arrays as follows 
array1 = np.array(["milk (l)", "cereals (packs)","quollfrisch (packs)"])
print(array1)
print(array1[0])


#so lets say we have the following three arrays
shopList = np.array(["milk (l)", "cereals (packs)","quollfrisch (packs)"])
quantList = np.array([3, 2, 5])
priceList = np.array([1.95, 2.05, 11.95])

# and want to combine them to a combined table, also known as a data frame
# we therefore first do all import the pandas package, a package which you will 
# come across quite frequently
import pandas as pd

# so lets create a shopping list data frame from our arrays 
# there are two ways to create the data frame depending on what you want the resutl to be 

# horizontal 
df1 = pd.DataFrame([shopList, quantList, priceList])

# vertical
df2 = pd.DataFrame({'item': shopList,'quantity': quantList, 'price': priceList}, columns = ['item', 'quantity', 'price'])

# when looking at both data frames we see the differences
print(df1)
print(df2)

# notice that the data frames are transposed versions of the other version

# we will continue with the second data frame
# lets add a new column which contains our expenses 
df2['expPerItem'] = df2['quantity'] * df2['price']
print(df2)

# lets export our new data frame as a .txt file
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

# however, easing future use we may also save our dataframe as a csv:
df2.to_csv("/Users/dominiquepaul/xJob/3-DataWithPythonCourse/allscripts/ourdata.csv")

