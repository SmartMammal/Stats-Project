import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import collections

# Loads the reduced version of the Lending Club Dataset
datalink = 'https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv'
loansData = pd.read_csv(datalink)

# Drop null rows
loansData.dropna(inplace=True)

# Break up the FICO
def getlowfico(x):
	x=x.split('-')
	return int(x[0])

loansData['FICO.Score'] = loansData['FICO.Range'].map(lambda x: getlowfico(x) )


# Take-out Percentage
def removepercentage(x):
	x = float(x[0:-1])
	return x

loansData['Interest.Rate'] = loansData['Interest.Rate'].map(lambda x: removepercentage(x) )

#TEST:
#print loansData['FICO.Range']
#print loansData['Interest.Rate']

# Plot historgram
plt.figure()
p = loansData['FICO.Score'].hist()
plt.show()

# Plot scatterplot matrix
#a = pd.scatter_matrix(loansData, alpha=0.05, figsize=(10,10)) #Plain
a = pd.scatter_matrix(loansData, alpha=0.05, figsize=(10,10), diagonal='hist') #Historgrams on diagnol
plt.show()

#Do regression
intrate = loansData['Interest.Rate']
loanamt = loansData['Amount.Requested']
fico = loansData['FICO.Score']

y = np.matrix(intrate).transpose() # The dependent variable
x1 = np.matrix(fico).transpose() # The independent variables shaped as columns
x2 = np.matrix(loanamt).transpose() # The independent variables shaped as columns
x = np.column_stack([x1,x2]) # Put the two columns together to create an input matrix

# Create a linear model
X = sm.add_constant(x)
model = sm.OLS(y,X)
f = model.fit()

#Print Results Summary Table
print f.summary() 

# Highlight Key Results
print 'Coefficients: ', f.params[1:2]
print 'Intercept: ', f.params[0]
print 'P-Values: ', f.pvalues
print 'R-Squared: ', f.rsquared