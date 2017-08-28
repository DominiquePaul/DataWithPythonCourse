#################
# Lecture 2 live
#################

# Topics of this lecture
# 1) Juggling with dataframes
# 2) Reading data from a website
# 3) Package
# 4) Loops
# 5) Drawing random numbers from a particular
#   distribution (if we get there)

# Install XML package
# Do this only once per machine!
# It's like an app
# install.packages("XML")

# Call the package/library
# Do this in every session
rm(list = ls())
library("XML")

shopList_0 = readHTMLTable("http://www.einkaufszettel.de/einkaufslisten/einkaufszettel-vorlage")
class(shopList_0)
shopList_0
## [1] "list"
# This is a list, new data type
length(shopList_0)
## [1] 2
# Select second list item
shopList = shopList_0[[2]]
class(shopList)
## [1] "data.frame"
class(shopList$V1)
## [1] "factor"
# The type of this variable is factor
# and we don't like that, for what we want to do
# We want "character"
shopList[] = lapply(shopList, as.character)
class(shopList$V1)
## [1] "character"
test1 = shopList[   1 , #rows 
                      ] #columns
                        # empty means ALL!
test1 = shopList[1, ]
class(test1)
## [1] "data.frame"
test2 = shopList[ , 1]
class(test2)
## [1] "character"
test3 = shopList[ , c(1,2)]

# delete row 1 and 18 from shopList
shopList = shopList[ -c(1,18) ,  ]

#columns to select
sel = seq(1, 9, by=2)

shopList1 = shopList[ , sel]

rm(list = ls(pattern = "^test"))

# Tests for getting all shopping items in one column
test1 = c(shopList$V1,
          shopList$V3,
          shopList$V5,
          shopList$V7,
          shopList$V9
          )


test1 = as.data.frame(test1)

test2 = c() #initialization
for (i in 1:ncol(shopList)){
  # Here is our algorithm
  test2 = c(test2, shopList[ , i])
}
test2 = as.data.frame(test2)

shopList = test2
class(shopList)
## [1] "data.frame"
# Change name of the single variable in shopList
names(shopList) = "item"
class(shopList$item)
## [1] "factor"
#Convert this to character
shopList[] = lapply(shopList, as.character)
class(shopList$item)
shopList[,1]
## [1] "character"
sink("inspectWhatWeAreDoing.txt", append=FALSE)
shopList$item == ""
##   [1] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
##  [12]  TRUE  TRUE  TRUE  TRUE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE
##  [23] FALSE FALSE FALSE FALSE  TRUE  TRUE  TRUE  TRUE  TRUE  TRUE  TRUE
##  [34]  TRUE  TRUE  TRUE  TRUE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE
##  [45] FALSE FALSE FALSE FALSE FALSE  TRUE  TRUE  TRUE  TRUE  TRUE FALSE
##  [56] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
##  [67] FALSE FALSE FALSE FALSE FALSE FALSE FALSE  TRUE  TRUE  TRUE FALSE
##  [78] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
##  [89] FALSE  TRUE  TRUE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
## [100] FALSE FALSE FALSE FALSE FALSE FALSE  TRUE  TRUE  TRUE  TRUE  TRUE
## [111]  TRUE  TRUE  TRUE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
## [122] FALSE FALSE FALSE FALSE FALSE FALSE  TRUE  TRUE  TRUE FALSE FALSE
## [133] FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
## [144] FALSE FALSE FALSE FALSE FALSE  TRUE  TRUE  TRUE  TRUE FALSE FALSE
## [155] FALSE FALSE FALSE FALSE FALSE FALSE FALSE  TRUE  TRUE  TRUE  TRUE
## [166]  TRUE  TRUE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
## [177] FALSE FALSE  TRUE FALSE FALSE  TRUE  TRUE  TRUE  TRUE  TRUE  TRUE
## [188]  TRUE  TRUE  TRUE
which(shopList$item == "")
##  [1]  12  13  14  15  16  27  28  29  30  31  32  33  34  35  36  37  38
## [18]  50  51  52  53  54  74  75  76  90  91  92 106 107 108 109 110 111
## [35] 112 113 114 128 129 130 149 150 151 152 162 163 164 165 166 167 168
## [52] 179 182 183 184 185 186 187 188 189 190
sink()
file.show("inspectWhatWeAreDoing.txt")

# In class, we got until here. 

# Now we still want to drop the empty rows from shopList
# In class, I still typed the following (how commented out with hashtags)

# shopList = shopList[-which(shopList$item == "") , ]

# This does not yield the desired result, for somewhat complicated reasons
# Let's not bother right now. 
# Instead, the following works

shopList = as.data.frame(shopList$item[-which(shopList$item == "") ])
names(shopList) = "item"