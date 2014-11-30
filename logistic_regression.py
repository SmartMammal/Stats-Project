import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import collections

# Loads the reduced version of the Lending Club Dataset
#loadlink = 'https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv'
#dumplink = '/Users/alihassan/Desktop/Thinkful/Projects/stats/loansData_clean.csv'

loadlink = '/Users/alihassan/Desktop/Thinkful/Projects/stats/loansData_clean.csv'
loansData = pd.read_csv(loadlink)

# Drop null rows
loansData.dropna(inplace=True)

# Create intercept column with value 1
loansData['Intercept'] = 1

#Get / Set independent column names
#ind_vars = list(loansData.columns.values)
ind_vars = ['Intercept', 'FICO.Score','Amount.Requested'] # Regress on FICO & loan amount requested

# Is Interest Rate less than 12?
loansData['IR_TF'] = loansData['Interest.Rate'].map(lambda x: bool(x < 12) )

#Run Model
logit = sm.Logit(loansData['IR_TF'], loansData[ind_vars])

#fit the model
result = logit.fit()

#Print Results Summary Table
#print result.summary()
#print result.params

# Break up the FICO
def logistic_function(a, b):
	e = 2.718
	p = 1 / (1 + e ** ( result.params[0] + result.params[1]*a + result.params[2]*b ) )
	return p

def pred(c):
	return bool(c > 0.7)

prob_acceptance = logistic_function(720, 10000)
isaccepted = pred(prob_acceptance)

# Notify Probability & Prediction of Acceptance
print "Given a 70% acceptance threshold, we predict..."
print "Probability Accepted:" + str(prob_acceptance)
print "Loan Accepted: " + str(isaccepted)