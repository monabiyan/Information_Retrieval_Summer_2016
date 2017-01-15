# Decision Tree Classifier
from sklearn import datasets
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm,linear_model
import numpy as np

import pandas as pd
import seaborn as sns



import matplotlib
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
# %matplotlib inline

# load the iris datasets
dataset = datasets.load_iris()
# fit a CART model to the data
model1 = DecisionTreeClassifier()
model2= svm.SVC()
model3= linear_model.LinearRegression()

X_TRAIN=np.array(dataset.data)      #example

model=model2
print(type(dataset.data))
model.fit(dataset.data, dataset.target)
print(model)
# make predictions
expected = dataset.target
predicted = model.predict(dataset.data)
# summarize the fit of the model
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

#######################################

link='http://www-bcf.usc.edu/~gareth/ISL/Advertising.csv'
data_xls=pd.read_csv(link,index_col=0)
print(data_xls.head(10))
print(data_xls.tail(10))
print(data_xls.shape)
plt.show()
sns.pairplot(data_xls,x_vars=['TV','Radio','Newspaper'],y_vars='Sales',kind='reg')
