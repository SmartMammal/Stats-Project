import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv') # gets Lending Club loan data
loansData.dropna(inplace=True) # removes rows with null values
colname = "Amount.Requested"

# Plot boxplot
loansData.boxplot(column=colname)
plt.show()

# Plot histogram
loansData.hist(column=colname)
plt.show()

# Plot against QQ
plt.figure()
graph = stats.probplot(loansData[colname], dist="norm", plot=plt)
plt.show()
