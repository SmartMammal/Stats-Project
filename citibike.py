import numpy as np 
import scipy.stats as stats
import pandas as pd # Let's look at the dataframe
import matplotlib.pyplot as plt # Let's plot the dataframe
from pandas.io.json import json_normalize # Get JSON data into a dataframe.
import statsmodels.api as sm
import requests # The requests library you need to get data off URL
import sqlite3 as lite # This library allows us to create and store table in a SQL database.
import time # a package with datetime objects
from dateutil.parser import parse # a package for parsing a string into a Python datetime object
import collections # Use this to build dictionary using defaultdict
import datetime

#Getting a a file off the internet:
#Documentation for requests package: http://docs.python-requests.org/en/latest/

r = requests.get('http://www.citibikenyc.com/stations/json') # get the data from a URL

"""
# A. Examine the data structure
print r.text # gives a basic view of text
r.json() # more structured view of the data
r.json().keys() # get the keys. keys help to call. This returns a list of keys available at a level and then navigate down
r.json()['executionTime'] # This allows you to see the executionTime list
len(r.json()['stationBeanList']) # Gets you the number of records (ie docks) in the system
r.json()['stationBeanList'][0] # the values in r.json()['stationBeanList'] are a list. Can access any element.
# Loop through, find all the keys (ie fields), print them out...
key_list = [] # a unique list of keys for each station listing
for station in r.json()['stationBeanList']:
    for k in station.keys():
        if k not in key_list:
            key_list.append(k)
print key_list
"""

# Get data into a dataframe.
df = json_normalize(r.json()['stationBeanList'])


"""
# B. Let's look at the dataframe
# Range of values for each attribute... available bikes frist
df['availableBikes'].hist()
plt.show()
# Range of total docks second
df['totalDocks'].hist()
plt.show()
# Matrix Scatter
#a = pd.scatter_matrix(loansData, alpha=0.05, figsize=(10,10)) #Plain
a = pd.scatter_matrix(df, alpha=0.05, figsize=(10,10), diagonal='hist') #Historgrams on diagnol
plt.show()
# Go through others...
# Figure out the Median and Mean
df['totalDocks'].mean()
df['totalDocks'].median()
# Figure out the Median and Mean of active stations
condition = (df['statusValue'] == 'In Service') # Set column with condition made of boolean for inservices
df[condition]['totalDocks'].mean() # Take mean of the intersection 
df[df['statusValue'] == 'In Service']['totalDocks'].median() # Here we put the condition inside the brackets.
"""

# Create a table and store it in a SQL database.

con = lite.connect('citi_bike.db')
cur = con.cursor()

# Clear the tables if they exist... start from scratch!
with con:
    deleteline = "DROP TABLE if exists citibike_reference"
    cur.execute(deleteline)
    deleteline2 = "DROP TABLE if exists available_bikes"
    cur.execute(deleteline2)

# This creates a table citibike_reference with a dozen or so columns.
# Use with as a context manager.
# At the end of indented code block, the transaction will commit (be saved) to the database.
# This is the same result as using con.commit()

with con:
    cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT )') 

#a prepared SQL statement we're going to execute over and over again. The INSERT INTO syntax looks like this...
# INSERT INTO table_name (column_name1, column_name2, column_name3, ...) VALUES (value1, value2, value3, ...)
# This is a parametrized query w/ ? standing in for values. 
sql = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"

#for loop to populate values in the database. For each station, use the SQL INSERT INTO statement:
with con:
    for station in r.json()['stationBeanList']:
    	# Take sql (the insert statement) and then puts the data in each record into the appropriate variable pockets
        #id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location)
        cur.execute(sql,(station['id'],station['totalDocks'],station['city'],station['altitude'],station['stAddress2'],station['longitude'],station['postalCode'],station['testStation'],station['stAddress1'],station['stationName'],station['landMark'],station['latitude'],station['location']))

#extract the column from the DataFrame and put them into a list
#add the '_' to the station name and also add the data type for SQLite
station_ids = df['id'].map(lambda x: '_' + str(x) + ' INT').tolist() 

#create the table
#in this case, we're concatentating the string and joining all the station ids (now with '_' and 'INT' added)
with con:
    cur.execute("CREATE TABLE available_bikes ( execution_time INT, " +  ", ".join(station_ids) + ");")

# Go through the loop 60 times (ie 1 minutes each loop per time.sleep function at bottom)
for i in range(60):
    r = requests.get('http://www.citibikenyc.com/stations/json') # get the data from a URL
    exec_time = parse(r.json()['executionTime']) #take the string and parse it into a Python datetime object
    
    cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%s'),)) # put the timestamp in
    con.commit()

    id_bikes = collections.defaultdict(int) #defaultdict to store available bikes by station

    #loop through the stations in the station list
    for station in r.json()['stationBeanList']:
        id_bikes[station['id']] = station['availableBikes']

    #iterate through the defaultdict to update the values in the database. k is the key and v is the value.
    for k, v in id_bikes.iteritems():
        cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime('%s') + ";")
    con.commit()

    time.sleep(60) # Pause for 1 minute (60 seconds) before going through the loop

df = pd.read_sql_query("SELECT * FROM available_bikes ORDER BY execution_time",con,index_col='execution_time')

hour_change = collections.defaultdict(int)
for col in df.columns:
    station_vals = df[col].tolist()
    station_id = col[1:] #trim the "_"
    station_change = 0
    for k,v in enumerate(station_vals):
        #enumerate() function returns not only the item in the list but also the index of the item.
        if k < len(station_vals) - 1:
            station_change += abs(station_vals[k] - station_vals[k+1])
    hour_change[int(station_id)] = station_change #convert the station id back to integer

def keywithmaxval(d):
    # create a list of the dict's keys and values; 
    v = list(d.values())
    k = list(d.keys())

    # return the key with the max value
    return k[v.index(max(v))]

# assign the max key to max_station
max_station = keywithmaxval(hour_change)

#query sqlite for reference information
cur.execute("SELECT id, stationname, latitude, longitude FROM citibike_reference WHERE id = ?", (max_station,))
data = cur.fetchone()
print "The most active station is station id %s at %s latitude: %s longitude: %s " % data

print "With " + str(hour_change[max_station]) + " bicycles coming and going in the hour between " + datetime.datetime.fromtimestamp(int(df.index[0])).strftime('%Y-%m-%dT%H:%M:%S') + " and " + datetime.datetime.fromtimestamp(int(df.index[-1])).strftime('%Y-%m-%dT%H:%M:%S')
#print "For the time between " + datetime.datetime.fromtimestamp(int(df.index[0])).strftime('%Y-%m-%dT%H:%M:%S') + " and " + datetime.datetime.fromtimestamp(int(df.index[-1])).strftime('%Y-%m-%dT%H:%M:%S')

plt.bar(hour_change.keys(), hour_change.values())
plt.show()

con.close() # close the database connection when done