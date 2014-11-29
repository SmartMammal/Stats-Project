import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd
import collections

# Load the reduced version of the Lending Club Dataset
loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

# Drop null rows
loansData.dropna(inplace=True)

# Put data into a collection
colname = 'Open.CREDIT.Lines'
freq = collections.Counter(loansData[colname])

# Print the distribution values
count_sum = sum(freq.values()) # calculate the number of instances in the list

for k,v in freq.iteritems():
  print "The frequency of number " + str(k) + " is " + str(float(v) / count_sum)

# Plot a bar chart
plt.figure()
plt.bar(freq.keys(), freq.values(), width=1)
plt.show()

# Perform Chi-Squared Test
chi, p = stats.chisquare(freq.values())

print "Chi-Squared = " + str(chi) + "\n"
print "P = " + str(p) + "\n"