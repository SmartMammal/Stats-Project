import time # a package with datetime objects
from dateutil.parser import parse # a package for parsing a string into a Python datetime object
import collections # Use this to build dictionary using defaultdict
import sqlite3 as lite # This library allows us to create and store table in a SQL database.
import requests # The requests library you need to get data off URL

# Connect to the database
con = lite.connect('citi_bike.db')
cur = con.cursor()

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

con.close() # close the database connection when done

import pandas as pd
import sqlite3 as lite

con = lite.connect('citi_bike.db')
cur = con.cursor()

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
print "With " + str(hour_change[379]) + " bicycles coming and going in the hour between " + datetime.datetime.fromtimestamp(int(df.index[0])).strftime('%Y-%m-%dT%H:%M:%S') + " and " + datetime.datetime.fromtimestamp(int(df.index[-1])).strftime('%Y-%m-%dT%H:%M:%S')

import matplotlib.pyplot as plt

plt.bar(hour_change.keys(), hour_change.values())
plt.show()






