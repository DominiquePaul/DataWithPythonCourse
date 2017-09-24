
########################################################################
# LECTURE 7: Get a function from a sepaarate file do the analysis!     #
########################################################################

# This is the fourth of the files for Lecture 7

rm(list = ls()) # Empty workspace to start with a "clean sheet"

# REPLACE THE WORKING DIRECTORY BELOW WITH THE ONE FOR YOUR DEVICE
#setwd("D:/Dropbox/Mac&Surf/Programmierkurs Dropb/Data")
setwd("/Users/dominiquepaul/xJob/1-DataWithPythonCourse/")


load("4-Data/dataforAnalysis.RData")

# NEW!!!
# This is how you call a function that you define in a
# separate file!
# It's like you wrote your own "package" and call it here!!!
source("2-R/lec7getAnalysis.R")

# Note on the path above:
# This is the example of a RELATIVE path

# My working directory is
# "D:/Dropbox/Mac&Surf/Programmierkurs Dropb/Data"
# This is where I have the data. However, my R scripts
# are in a different directory:
# "D:/Dropbox/Mac&Surf/Programmierkurs Dropb/R_Scripts"
# So, starting from the Data directory, I have to go 
# one directory up, and then down to R_Scripts.
# This is what "../R_Scripts/getAnalysis.R" means.


getAnalysis(currency = unique(dataXrates$D1)[2], 
            tradeDirection = "Ausfuhr", 
            typeOfGoods = "Total", 
            measure = "Wert in Millionen Franken",
            saveGraph = "yes"
)

# Now we want to start massproduction of graphs!
# Create a folder inside your working directory,
# call it plots

typeList = unique(dataAussen$D1[dataAussen$D0 == "Ausfuhr"])

# This is a list we want to loop over to get all the
# respective plots
# Note that not all values in dataAussen$D1 are available for 
# "Ausfuhr". Some are only available for "Einfuhr". This
# explains the slightly more involved code above.

for (i in typeList){
  getAnalysis(currency = unique(dataXrates$D1)[1], 
              tradeDirection = "Ausfuhr", 
              typeOfGoods = i, 
              measure = "Wert in Millionen Franken",
              saveGraph = "yes"   # TURN THIS ON!!!!
  )
}

# If you are not yet impressed, then lets expand capacity!
currList = unique(dataXrates$D1)


for (i in currList){
  for (j in typeList[2:length(typeList)]){
    
    currency = i
    tradeDirection = "Ausfuhr"
    typeOfGoods = j 
    
    cat("\\subsection{Reaktion von ", tradeDirection,
        " (", typeOfGoods, ") auf ", currency,
        "-Wechselkurs}", sep = "")
    
    getAnalysis(currency, 
                tradeDirection, 
                typeOfGoods, 
                measure = "Wert in Millionen Franken",
                saveGraph = "yes"
    )
  }
}

# The best way to inspect the output is to open a new word document 
# and drag the files into that document from the file explorer/finder.  


# This is all pretty cool. There is one drawback of this procedure, 
# however. We cannot automate any text comments on our results,
# nor automate the printing and commenting of regression results.

# In order to automate documentation further, we need an additional
# tool: RMarkdown!

