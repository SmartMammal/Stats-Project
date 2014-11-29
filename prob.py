import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt
import collections

x = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 9, 9]
c = collections.Counter(x)

print c # Print the data

# Print the distribution values
count_sum = sum(c.values()) # calculate the number of instances in the list

for k,v in c.iteritems():
  print "The frequency of number " + str(k) + " is " + str(float(v) / count_sum)

# Plot boxplot
plt.boxplot(x)
plt.show()

# Plot histogram
plt.hist(x, histtype='bar')
plt.show()

# Plot against QQ
plt.figure()
graph1 = stats.probplot(x, dist="norm", plot=plt)
plt.show()
