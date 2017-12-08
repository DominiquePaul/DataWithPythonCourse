
# Description -------------------------------------------------------------

# A brief tour through the most important features of R and R Studio that
# you need for getting started.

# Creating an R project ---------------------------------------------------

# Do the following steps:
# Create a folder where you put everything in that belongs to 
# this course (I suggest "Data Science Fun"). 
# Create an R project using File/New Project in RStudio. Through this function,
# create a new folder called "Programming" inside the overall folder
# for this course.
# Then close RStudio and navigate to that directory.
# You will see an item that ends with ".Rproj".
# To start working with R, either double click on that item; 
# or open RStudio, go to the file menu, choose "Open Project"
# and select the same ".Rproj" item mentioned above.
# Or start a project that you had already opened recently on the upper-
# right cornder of RStudio.
# Always start a session in R with the respective project!
# You will see why a little later.



# Some important features of RStudio --------------------------------------

# Note: Always work with RStudio, never with R directly!

# 1) Scripts and sections in scripts 
#       (See Chapter 4 "Workflow: Scripts" in the book, or http://r4ds.had.co.nz/workflow-scripts.html)
# 2) The various panes of RStudio
# 3) Global Options
# 4) Always work with scripts that you can save!!!


# Packages ----------------------------------------------------------------

# Packages provide additional "functions" (or functionality) for R beyond
# what you have acquired with a baseline installation. There are several
# good reasons why not every function that exists is downloaded with a 
# base installation. Since we use the functionality as instructed in the 
# book "R for Data Science", we first need to load some packages.

# Imagine that packages are like "apps" (e.g. for the programming
# environment "Android") or "plugins" (e.g. like in Excel or Word).


# Install the package "tidyverse". Do this only *once*! 
# (Do it every time you newly installed R on a machine. It's really like an app!)

#install.packages("tidyverse")

# Immediately "comment" the installation command out, so it will not get
# reinstalled every time you run the code from this file!

# Unlike an app, you need to activate ("call") the functionality of
# a package for every session
library(tidyverse)

# You'll get some comments in red. That's normal. 
# Some packages have functions with the same name.
# If you load packages that have functions with the
# same name as a function in the baseline version,
# then that baseline version get's "masked". 
# For instance, the stats package belongs to the
# base version of R and contains functions called
# filter() and lag(). The dplyr package (included 
# in the tidyverse) contains functions with the same 
# names. If you call the tidyverse and run filter(), 
# R will use the version from the dplyr package.

