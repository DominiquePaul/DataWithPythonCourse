#############
# Functions #
#############

import string 
import numpy as np

# in python, indentions are often used instead of brackets
def say_hello(name):
	print("Hello " + name + ", how are you doing today")

say_hello("Sabrina")

say_hello("Christian")

list1 = list(string.ascii_lowercase)
for letter in list1:
	say_hello(letter)

# The input values for the calculation
spending = 5000
interest_rate = 4
t = 30
say_hello
# The stupid way to program... 
# (this does not even deserve the name "programming")

pv_spending = 5000/1.04**30
print(pv_spending)

# The smartest way: Using functions

def save_fun1(x, r, t):
	output = round(x/(1+r/100)**t, 
		2) #sets the amount of decimals we want to round to
	print(output)

save_fun1(5000, 0, 30)

# Label arguments
def save_fun2(spending, interest_rate, horizon):
	x = spending
	r = interest_rate
	t = horizon

	output = round(x/(1+r/100)**t, 2) 
	print(output)

save_fun2(spending = 5000, interest_rate = 4,
        horizon = 30)
## [1] 1542
save_fun2(horizon = 30, spending = 5000, interest_rate = 4)
## [1] 1542
save_fun2(30, 5000, 4)

# With labels you can change the order of the arguments,
# without labels, you cannot.

# Lets give the arguments default values
def save_fun3(spending = 5000, 
	interest_rate = 4, 
	horizon = 30):

	x = spending
	r = interest_rate
	t = horizon

	output = round(x/(1+r/100)**t, 2) 
	print(output)

save_fun3()

save_fun3(spending = 1000)

def save_fun4(spending = 5000, 
	interest_rate = 4, 
	horizon = 30,
	get_out_as_text = None):
	
	x = spending
	r = interest_rate
	t = horizon

	output = round(x/(1+r/100)**t, 2)
	print(output)

	if get_out_as_text != None:
		# %d is a placeholder for a number. %.2f is for a float and the 2 indicates 
		# the number of decimals. The placeholder for a string is %s
		print("If you want to spend %d after %d years and the interest rate is %d you have to save %.2f" % (x,t,r,output)) 
		# This is however an old-fashioned way of formatting a string 
		# and will eventually removed from newer python versions.
		# Therefore, lets have a look at newer ways of doing this:
		# print("If you want to spend {} after {} years and the interest rate is {} you have to save {}".format(x,t,r,output))

save_fun4(get_out_as_text = 1)


