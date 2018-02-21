import perceptron2_package as perc
import pandas as pd
from sklearn.utils import shuffle
import numpy as np


perc.test_package()


wdbc = pd.read_csv("/Users/dominiquepaul/xJob/DataWithPythonCourse1/Data/wbdc.csv")
wdbc.replace(["M","B"],[0,1], inplace = True)

perc_train = 0.7

wdbc = shuffle(wdbc, random_state = 1).reset_index().drop(["index"],axis=1)
wdbc.head()

#split the set into training and test set
training_set_wdbc = wdbc.iloc[0:round(perc_train*len(wdbc)),:]
test_set_wdbc = wdbc.iloc[round(perc_train*len(wdbc)):,:]



x = perc.perceptron(0.01)
x.fit(training_set_wdbc.iloc[:,3:33].values, training_set_wdbc.iloc[:,2].values)
 
# print(x.weightsdf_.head())

evaluation = test_set_wdbc
evaluation["result"] = np.where(evaluation.iloc[:,2] == x.predict(test_set_wdbc.iloc[:,3:33].values), 1, 0)
corrects = evaluation["result"].sum()
estimations_made = len(evaluation["result"])
fraction_correct = corrects / estimations_made
print("The Perceptron algorithm classified {0:.3f}% of the test data correctly".format(fraction_correct))





