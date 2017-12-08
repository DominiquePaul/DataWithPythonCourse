

# The third file for Lecture 7

# This file just contains a copy-cat version of the 
# function definition in Lec7_2.R !
# Well, a very few things are either removed or rearranged.
# But it's basically a carbon copy!

# important: we keep the import statements as well as the lines loading the data
# as the function relies on them
# alternatively, we could include additional arguments in the function passing the data 
# on to the function

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.formula.api as smf
import colorama
from colorama import Fore, Back, Style




# REPLACE THE WORKING DIRECTORY BELOW WITH THE ONE FOR YOUR DEVICE
os.chdir("/Users/dominiquepaul/xJob/1-DataWithPythonCourse/4-Data/")
data_xrates = pd.read_csv("dataforanalysis_xrates.csv", sep = ",", index_col = 0)
data_aussen = pd.read_csv("dataforanalysis_aussen.csv", sep = ",", index_col = 0)

# this changes the figure size which is relevant when we will convert to pdf
plt.rcParams['figure.figsize'] = (10,10)

def get_analysis(currency, trade_direction,
 type_of_goods, measure, start_year = 2000, 
 data_as_change_rates = True, save_graph = False):

	curr = currency 
	trade_dir= trade_direction
	goods_type = type_of_goods


	# This parameter determines whether data should
	# be analysed in levels or percentage change rates

	########################################

	# The function to convert data to percentage
	# change rates, like in Lecture 6

	def to_growth(series):
		#we have to reset the index as pandas will otherwise divide
	    # all rows which have the same index, which would mean that all 
	    # results would be zero
	    out = (series.tail(-1).reset_index(drop = True) / series.head(-1) -1 ).reset_index(drop = True) * 100
	    # This is one element shorter than input, 
	    # add an NA as first value
	    df1 = pd.DataFrame([None])
	    # 'ignore_index' means that the two DFs are merged while neglecting 
	    # any order of their indices 
	    out = pd.concat([df1, out], ignore_index = True)
	    return out

	# Select the subset of rows and columns from 
	# dataAussen and dataXrates that we need,
	# assign new name to resulting object.

	# we use @ when referencing variables in the string
	aussen = data_aussen.query("D0 == @trade_dir and D1 == @goods_type and D2 == @measure and timeID >= @start_year")[["timeID", "D0","D1","D2", "Value"]]
	# print(aussen.head())

	xrates = data_xrates.query("D1 == @curr and timeID >= @start_year")[["timeID","D1", "Value"]]
	# print(xrates.head())

	# we bring our data into wide format

	xrates = xrates.pivot(index = "timeID", columns = "D1",  values = "Value").reset_index()

	aussen["join"] = aussen["D0"] + "_" + aussen["D1"] + "_" + aussen["D2"]
	aussen = aussen.pivot(index="timeID", columns="join", values = "Value").reset_index()


	# quite some new stuff from here on !
	# make variable name for variable in "aussen" prettier, such that we can use it for labels in graphs
	# In particular, we do not want the underscores and not "in Millionen Franken".
	x = aussen.columns[1].rfind("_") # find the last position of an underscore

	# cut off the pieces after the last underscore
	# ("Wert in Millionen Franken")
	new_name = aussen.columns[1][0:x]

	# replace all instances of _ by -  in our string
	new_name = new_name.replace("_","-")

	# replace columns name
	aussen =  aussen.rename(columns = {aussen.columns[1]:new_name})

	# NOTE: All this code works for ANY type of export/import variable
	# we may want to analyse. It is GENERIC. That's why it's a little 
	# tedious to write, but it ALWAYS works.
	# Compare this to a "manual" specific adjustment without the stringr
	# commands. This would only work for ONE SPECIFIC case, not ALL!!!

	data = pd.merge(xrates, aussen, # the DFs which we want to merge
	 on='timeID') # the column by which we wont to merge the DFs

	# rename "timeID" to something that looks pretty in a graph
	data = data.rename(columns = {aussen.columns[0]: "Zeit"})

	# convert to rate of change, if required by parameter dataAsChangeRates

	# For this to work for any of our potential variables
	# we need a generic names for the thing in the third column of D.
	# In the regression analysis, this will be our y-variable.
	yvar = data.columns[2]

	# convert to percentage changes
	if data_as_change_rates:
		data[curr] = to_growth(data[curr])
		data[yvar] = to_growth(data[yvar])

	# One more piece about the variable names to make them useful for labels in graphs.
	# If we change the data to percentage changes we want to be able to get this in the graphs
	# from the labels, otherwise, we may forget whether we plotted levels or change rates

	data.head() #asdf

	add_to_lab = ""  # initialize an empty character variable

	# make it nonempty in case that we convert data to percentage changes

	if data_as_change_rates:
		add_to_lab = "(Veränderung in \u0025)"

	# the "\u0025" code is an example of UTF-8 encoding
	# See http://www.utf8-chartable.de/unicode-utf8-table.pl?utf8=oct&unicodeinhtml=dec&htmlent=1

	# Preparing orderly file names
	# for option of saving graphs to file
	######################################

	# NEW

	# Create a folder inside your working directory,
	# call it plots

	# We want to have file names that indicate all parameters, such
	# as "CHFproEuro_Ausfuhr_Total_WertNom_Veraend"
	# If you then want to select a few graphs for
	# your document (e.g. thesis), you can quickly identify
	# the one you want.
	# This code is run ONLY IF saveGraph is "yes"

	if save_graph:
		x = "" # This is becoming the piece that replaces "Wert in Millionen Franken",
		# in case that measure takes on this value. Otherwise, x stays empty (i.e. "")
		if measure == "Wert in Millionen Franken":
			x = "WertNom"
			if data_as_change_rates:
				x = x + "_Veraend"
				# if data are converted to percentage changes add this to x

	# Now put all the pieces together, separated by
	# underscores, which are practical for the purpose of file names

		fname = "_".join([curr, trade_dir, goods_type, x])
		fname = fname.replace("/", "pro")
		fname = "plots/" + fname
		print(fname)




	# Analysis
	########################################

	fig = plt.plot(data[curr], data[yvar],
	 "b.", # we set the visualisation to blue dots
	 ms=4 ) # the markersize, the size of the dots
	plt.grid() 
	# add labels
	plt.xlabel(" ".join([curr,add_to_lab]))
	plt.ylabel("\n".join([trade_dir, goods_type, add_to_lab])) # we use "\n" as a separater 
	# between the arguments of paste. This means a line break! 
	# the title of the graph
	plt.title(trade_dir + " (" + goods_type + ") \n und " + curr + "-Wechselkurs" )


	# Add a OLS regression line of best fit

	# we check which data rows have values which we can use
	idx = np.isfinite(data[curr]) & np.isfinite(data[yvar])
	# determine our slope and y-intercept 
	m,c = np.polyfit(data[curr][idx], data[yvar][idx],1)

	plt.plot(data[curr], 
	         m*data[curr] + c,   # our y-values in the form of a linear equation
	         'r-',      # a solid red line 'r' => red; '-' => solid line
	         lw = 0.8   # set the line width
	         ) 
	plt.show() #asdf


	# save our figure our folder
	if save_graph: 
		plt.savefig(fname + ".png", bbox_inches='tight') 
	# the bbox setting adjusts the margins so that all text is visible
	plt.close()



	# we run a regression and save it under 'results'
	results = smf.OLS(data[yvar][idx], data[curr][idx]).fit()

	# We can now inspect the results as usual with the command
	print("Die zugehoerige Regressionstabelle sieht wie folgt aus.\n\n")
	print(results.summary())



	# but what if we only want one of the values at hand?
	# we can inspect the attributes and functions of the object by using the command
	# print(dir(results)) #asdf



	# Some text output for later use
	print("\n\nDas R^2 betraegt " + str(round(results.rsquared, 3)) + ".")

	# we can easily extract the pvalue that tells us
	# whether the estimated relationship is statistically significant
	pval = results.pvalues[0]

	# we use the colorama package to change the text of our output, 
	# attention: this only works when we execute the code in the terminal
	# to run code in your terminal, just open your terminal enter_: "python3 " 
	# drag in your file and from the finder at hit enter
	colorama.init()


	# this changes the color of our text depending on whether 
	# the statistical relationship is significant
	if pval < 0.05:
		print(Fore.GREEN + "Die Beziehung ist statistisch signifikant!" + Style.RESET_ALL)
	else:
		print(Fore.RED + "Wir haben hier keine statistisch signifikante Beziehung." + Style.RESET_ALL)
