
############################################
# LECTURE 4, Part 1: Completing function   #
# from last time with an optional argument #
############################################

# During Lecture 3 we worked on a function with an optional
# or "NULL" argument: if the argument get.out.as.text is not NULL,
# then the function saveFun would get the output as text.

x = 5000; t = 30; r = 4

out = round(x/(1+r/100)**t)

output1 = "If you want to spend {} after {} years and the interest rate is {} percent, you have to save {}.".format(x, t, r, out)     
print(output1)


# if you want to perform a line break in Python you can break it up into 
# two parts and put a '\' after the end of the first line

output1 = "If you want to spend {} after {} years and the interest " \
            "rate is {} percent, you have to save {}.".format(x, t, r, out)       
print(output1)

# as you will see there is no difference


# you can of course also print this directly
print("If you want to spend {} after {} years and the interest rate is {} percent, you have to save {}.".format(x, t, r, out))

# so we know the format method so far
# you can also use indexes to save time
output2 = "If you want to spend {0} after {1} years and the interest rate is {2} percent, you have to save {3}.".format(x, t, r, out)
print(output2)
# this can be useful if you have reocurring elements

#if you don't want to count, you can also just use keywords
output3 = "If you want to spend {amountToSpend} after {years} years and the interest rate is {interestRate} percent, you have to save {savingAmount}.".format(amountToSpend = x,years = t,interestRate = r, savingAmount = out)            
print(output3)


##############
# conditionals
##############

# In Python, if-conditions do not have to be put into brackets
# the ensuing command is written after a double colon after the statement
# indentation is important, indentate your commands by using the tabulator key

arg = "no"

if arg == "no": 
    print("I have nothing to say :-(")
    

# So what if arg = "yes"?
arg = "yes"

if arg == "no":
    print("I have nothing to say :-(")

#we can also use else if or else statements to tell the program to 
#do if the first condition is not fulfullled

arg = "no"

if arg == "no":
    print("I have nothing to say :-(")
elif arg == "alternativeString": #this command is if we want to include more than one statement
    print("Alternative Output")
else: #this command is optional too
    print(":-))")


# Now let's make a function out of this
# Use "def" to create new functions
# again: since we are not using curly brackets as with other languages,
# be sure to indent the content of your function correctly

def saySomething(arg):
    if arg == "no": 
        print("I have nothing to say :-(")
    elif arg == "yes":
        print(":-))")
    
# we can now invoke our function like this
saySomething("no")
saySomething("yes")


############################################
# Now lets go back to our savings function:
############################################

# In Python we use None to declare an empty variable, similar as we do
# with NULL in R
a = None 
b = "yes"

# we can check whether a function is empty by using 'is'; this will return a boolean
print(a is None)
print(b is None)

def saveFun(spending = 5000, interestRate = 4, horizon = 30, getText = None):
    x = spending
    r = interestRate
    T = horizon
    out = round(x/(1+r/100)**T)
    
    if getText is None:
        return(out)
        # everything in a function that comes after return is not executed
        # if return is executed...
    elif getText == "yes" :
        print("If you want to spend {} after {} years and the interest rate is {} percent, you have to save {}.".format(x, T, r, out))

saveFun()

saveFun(getText= "yes")

saveFun(spending = 5000, interestRate = 1, horizon = 30, getText = "yes")

saveFun(spending = 5000, interestRate = -0.5, horizon = 30)




######################################################
# EXTRA CODE: Creating an interactive program
######################################################


# Other than in R we can also make the program interactive and ask the user for input
# One way of doing this is using the function 'input' to assign new values to our variables
# Because the input is taken as a string, we use the functions int() or float() to convert the string input to an integer or float

def saveFunInteractive(spending = 5000, interestRate = 4, horizon = 30, getText = "yes"):
    x = int(input("How much do you want to spend? (e.g. 7500) "))
    r = float(input("What is the interest rate you want to use? (e.g. 3.5) "))
    T = int(input("How long is your time horizon? (e.g. 5) "))
    out = round(x/(1+r/100)**T)
    
    if getText is None:
        return(out)
        # everything in a function that comes after return is not executed
        # if return is executed...
    else:
        print("If you want to spend {} after {} years and the interest rate is {} percent, you have to save {}.".format(x, T, r, out))

saveFunInteractive()











