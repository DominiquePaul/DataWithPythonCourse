#############
# Functions #
#############

sayHello = function(name){
  paste0("Hello ", name,
         ", how are you doing today?")
}

sayHello("Sabrina")
## [1] "Hello Sabrina, how are you doing today?"
sayHello("Christian")
## [1] "Hello Christian, how are you doing today?"
LETTERS
##  [1] "A" "B" "C" "D" "E" "F" "G" "H" "I" "J" "K" "L" "M" "N" "O" "P" "Q"
## [18] "R" "S" "T" "U" "V" "W" "X" "Y" "Z"
sayHello(LETTERS)
##  [1] "Hello A, how are you doing today?"
##  [2] "Hello B, how are you doing today?"
##  [3] "Hello C, how are you doing today?"
##  [4] "Hello D, how are you doing today?"
##  [5] "Hello E, how are you doing today?"
##  [6] "Hello F, how are you doing today?"
##  [7] "Hello G, how are you doing today?"
##  [8] "Hello H, how are you doing today?"
##  [9] "Hello I, how are you doing today?"
## [10] "Hello J, how are you doing today?"
## [11] "Hello K, how are you doing today?"
## [12] "Hello L, how are you doing today?"
## [13] "Hello M, how are you doing today?"
## [14] "Hello N, how are you doing today?"
## [15] "Hello O, how are you doing today?"
## [16] "Hello P, how are you doing today?"
## [17] "Hello Q, how are you doing today?"
## [18] "Hello R, how are you doing today?"
## [19] "Hello S, how are you doing today?"
## [20] "Hello T, how are you doing today?"
## [21] "Hello U, how are you doing today?"
## [22] "Hello V, how are you doing today?"
## [23] "Hello W, how are you doing today?"
## [24] "Hello X, how are you doing today?"
## [25] "Hello Y, how are you doing today?"
## [26] "Hello Z, how are you doing today?"
# A function that calculates saving needs for retirement
########################################################

# The input values for the calculation
spending = 5000
interestRate = 4
T = 30

# The stupid way to program... 
# (this does not even deserve the name "programming")

pvSpending = 5000/1.04^30
pvSpending
## [1] 1541.593
# A little smarter with using variables

pvSpending = spending/(1+interestRate/100)^T

# The smartest way: Using functions

saveFun = function(x, r, T){
  round(  x/(1+r/100)^T  )
}
saveFun(5000, 0, 30)
## [1] 5000
# Label arguments
#################

saveFun = function(spending, interestRate,
                   horizon){
    x = spending
    r = interestRate
    T = horizon
  round(  x/(1+r/100)^T  )
}

saveFun(spending = 5000, interestRate = 4,
        horizon = 30)
## [1] 1542
saveFun(horizon = 30, spending = 5000,
        interestRate = 4)
## [1] 1542
saveFun(30, 5000, 4)
## [1] 0
# With labels you can change the order of the arguments,
# without labels, you cannot.

# Default values
#################

saveFun = function(spending = 5000,
                   interestRate = 4,
                   horizon = 30){
  x = spending
  r = interestRate
  T = horizon
  round(  x/(1+r/100)^T  )
}

saveFun()
## [1] 1542
saveFun(spending = 1000)
## [1] 308
# Optional arguments
####################

# !!! WARNING: THE CODE BELOW IS INCOMPLETE, 
#     WE WILL FINISH THIS THE NEXT TIME!!!!

saveFun = function(spending = 5000,
                   interestRate = 4,
                   horizon = 30,
                   get.out.as.text = NULL){
  x = spending
  r = interestRate
  T = horizon
  out = round(  x/(1+r/100)^T  )

  if(  !is.null(get.out.as.text)  ){
    cat(sprintf("If you want to spend %s after %s years
and the interest rate is %s percent, 
you have to save %s.", x, T, r, out))
  }


}

x = 5000; T = 30; r = 4