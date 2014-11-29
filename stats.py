import pandas as pd

data = '''Region, Alcohol, Tobacco
North, 6.47, 4.03
Yorkshire, 6.13, 3.76
Northeast, 6.19, 3.77
East Midlands, 4.89, 3.34
West Midlands, 5.63, 3.47
East Anglia, 4.52, 2.92
Southeast, 5.89, 3.20
Southwest, 4.79, 2.71
Wales, 5.27, 3.53
Scotland, 6.08, 4.51
Northern Ireland, 4.02, 4.56'''

# First, split the string on the (hidden characters that indicate) newlines
data = data.splitlines() # we could also do data.split('\n')

# Then, split each item in this list on the commas
# the bracketed expression is a list comprehension
data = [i.split(', ') for i in data] 

# Now, convert create a pandas dataframe
column_names = data[0] # this is the first row
data_rows = data[1::] # these are all the following rows of data
df = pd.DataFrame(data_rows, columns=column_names)

# There's no built-in mode method in Python, so we need scipy.stats
from scipy import stats

# Convert Alcohol and Tobacco columns to float
df['Alcohol'] = df['Alcohol'].astype(float)
df['Tobacco'] = df['Tobacco'].astype(float)

# A function that calculates and prints descriptive stats summary...
def print_sum (col_name): 
	intro = "For " + col_name + "...\nThe mean, median, mode, range, variance, and standard deviation are as follows: "
	intro += str(df[col_name].mean())
	intro += ", " + str(df[col_name].median())
	intro += ", " + str(float(stats.mode(df[col_name])[0]))
	intro += ", " + str(max(df[col_name]) - min(df[col_name]))
	intro += ", " + str(df[col_name].var())
	intro += ", and " + str(df[col_name].std()) 
	intro += ". \n"
	print intro

# Run the functions
print_sum('Alcohol')
print_sum('Tobacco')

