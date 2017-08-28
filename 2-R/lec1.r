# R live script, Lecture 1, Feb 25, 2016

a = 2
a
## [1] 2
# Variables have types. Let's see what's
# the type of a...
class(a)
## [1] "numeric"
# Are there other types?
aAsChar = "a"
aAsChar
## [1] "a"
class(aAsChar)
## [1] "character"
#Go on...
b = 3 
bAsWhatever = b
bAsWhatever
## [1] 3
# Let's do some algebra
a+b
## [1] 5
a*b
## [1] 6
a^b
## [1] 8
i <- 1  # Assignment operator
        # same as "=", the latter is also assignment operator
i = 1
j = i  # passed by value
i = 2
# What will j be?
j
## [1] 1
i == j # this is nothing else as 2 == 1
## [1] FALSE
# "=" is an assignment operator
# "==" means mathematical equality

l = i ==j
l
## [1] FALSE
class(l)
## [1] "logical"
######################################################
######################################################

# Beyond the most basic data structures
shopList = c("milk (l)", "cereals (packs)",
             "quollfrisch (packs)")

# shopList is a vector

quantList = c(3, 2, 5)

priceList = c(1.95, 2.05, 11.95)

shoppingData = data.frame(shopList, quantList, priceList)

class(shoppingData)priceList
## [1] "data.frame"
shoppingData$expPerItem =
  shoppingData$quantList*shoppingData$priceList

sink("myShopList.txt", append = FALSE)
shoppingData
##              shopList quantList priceList expPerItem
## 1            milk (l)         3      1.95       5.85
## 2     cereals (packs)         2      2.05       4.10
## 3 quollfrisch (packs)         5     11.95      59.75
sink()
file.show("myShopList.txt")