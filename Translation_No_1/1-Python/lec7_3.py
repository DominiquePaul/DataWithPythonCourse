import os
import pandas as pd



os.chdir("/Users/dominiquepaul/xJob/1-DataWithPythonCourse/4-Data/")

data_xrates = pd.read_csv("dataforanalysis_xrates.csv", sep = ",", index_col = 0)
data_aussen = pd.read_csv("dataforanalysis_aussen.csv", sep = ",", index_col = 0)

# remember to change the directory if your scripts are in other places than your data
os.chdir("/Users/dominiquepaul/xJob/1-DataWithPythonCourse/1-Python")

from lec7getAnalysis2 import get_analysis

get_analysis(currency = data_xrates.ix[:,"D1"].unique()[2],
	trade_direction = "Ausfuhr", 
    type_of_goods = "Total", 
    measure = "Wert in Millionen Franken",
    save_graph = False)

# Now we want to start massproduction of graphs!
# Create a folder inside your working directory,
# call it plots

typelist = data_aussen.ix[data_aussen.ix[:,"D0"] == "Ausfuhr","D1"].unique()

for i in typelist: 
	currency = data_xrates.ix[:,"D1"].unique()[0]
	trade_direction = "Ausfuhr"
	type_of_goods = i

	get_analysis(currency,		
              trade_direction, 
              type_of_goods, 
              measure = "Wert in Millionen Franken",
              save_graph = False)




curr_list = data_xrates.ix[:, "D1"].unique()

# typelist = typelist[1:len(typelist)]

# for i in curr_list:
# 	for j in typelist[1:len(typelist)]:
# 		currency = i
# 		trade_direction = "Ausfuhr"
# 		type_of_goods = j

# 		print("\\subsection{Reaktion von " + trade_direction + " (" + type_of_goods, ") auf " + currency + "-Wechselkurs}")
# 		get_analysis(currency = i, trade_direction = "Ausfuhr", type_of_goods = j, measure = "Wert in Millionen Franken", save_graph = True)


# The best way to inspect the output is to open a new word document 
# and drag the files into that document from the file explorer/finder.  


# This is all pretty cool. There is one drawback of this procedure, 
# however. We cannot automate any text comments on our results,
# nor automate the printing and commenting of regression results.

# In order to automate documentation further, we need an additional tools


