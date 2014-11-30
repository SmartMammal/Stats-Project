import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import collections

# Loads the full version of the Lending Club Dataset
loadlink = '/Users/alihassan/Desktop/Thinkful/Projects/stats/LoanStats3c.csv'
loansData = pd.read_csv(loadlink, header=1, skiprows=0)

#Take a look at the dataset
#print loansData.head(3)
#print loansData.tail(3)
#print loansData.columns.values
#print loansData.describe()
#print loansData['int_rate'].head()

# Drop null rows
loansData.dropna(inplace=True)

# Create intercept column with value 1
loansData['Intercept'] = 1

# Clean Data: For Interest Rates, Remove Percentage
def removepercentage(x):
	x = float(x[0:-1])
	return x

loansData['int_rate'] = loansData['int_rate'].map(lambda x: removepercentage(x) )
#print loansData['int_rate'].head()

# Clean Data: Handle Home Ownership Data Info... split into 4 dummy variables
loansData['home_rented'] = loansData['home_ownership'].map(lambda x: bool(x == "RENT") )
loansData['home_owned'] = loansData['home_ownership'].map(lambda x: bool(x == "OWN") )
loansData['home_mortgaged'] = loansData['home_ownership'].map(lambda x: bool(x == "MORTGAGE") )
loansData['home_other'] = loansData['home_ownership'].map(lambda x: bool(x == "OTHER") )
#print loansData['home_ownership'].head()
#print loansData['home_rented'].head()

# Create Interaction Variable between Home Ownership & Incomes
loansData['home_owned_x_annual_inc'] = loansData['home_owned'] * loansData['annual_inc']
#print loansData['home_owned_x_annual_inc'].head(25)

#Get / Set independent column names
#ind_vars = list(loansData.columns.values)
ind_vars1 = ['Intercept', 'annual_inc'] # Regress on annual income only
ind_vars2 = ['Intercept', 'annual_inc', 'home_owned'] # Regress on annual income & homeownership variables
ind_vars3 = ['Intercept', 'annual_inc', 'home_owned', 'home_owned_x_annual_inc'] # Regress on annual income & homeownership variables

#Run, Fit and Print Model #1
model1 = sm.OLS(loansData['int_rate'], loansData[ind_vars1])
result1 = model1.fit()
print "\n *** MODEL: ANNUAL INCOME ***"
print result1.summary()
#print result1.params

#Run, Fit and Print Model #2
print "\n *** MODEL: ANNUAL INCOME & HOME OWNERSHIP ***"
model2 = sm.OLS(loansData['int_rate'], loansData[ind_vars2])
result2 = model2.fit()
print result2.summary()
#print result2.params

#Run, Fit and Print Model #3
print "\n *** MODEL: ANNUAL INCOME & HOME OWNERSHIP & INTERACTION THEREOF***"
model3 = sm.OLS(loansData['int_rate'], loansData[ind_vars3])
result3 = model3.fit()
print result3.summary()
#print result2.params