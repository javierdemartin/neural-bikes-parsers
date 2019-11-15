import urllib.request
import os.path
import json
import datetime
import os
import pytz

tz = pytz.timezone('Europe/Madrid')
now = datetime.datetime.now(tz)

dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"

print(dir_path)

if os.path.exists(dir_path + "../data/bilbao.csv") == False:

    f= open(dir_path + "../data/bilbao.csv" ,"w+")
    f.write("date,id,station_name,free_bikes,free_docks\n")
    f.close()

date = datetime.datetime.now()
date = now.strftime('%Y-%m-%dT%H:%M:%SZ')

url = "https://nextbike.net/maps/nextbike-official.json?city=532"

jsonData = urllib.request.urlopen(url)
jsonObject = json.load(jsonData)

jsonObject = jsonObject['countries'][0]['cities'][0]['places']

parsedAvailability = ""

idString = "number"
stationNameString = "name"
freeBikesString = "bikes"
freeRacksString = "free_racks"

for station in jsonObject:

    stationAvailablity = ""

    stationAvailablity += str(date) + ","
    stationAvailablity += str(station[idString]) + ","
    stationAvailablity += station[stationNameString] + ","
    stationAvailablity += str(station[freeBikesString]) + ","
    stationAvailablity += str(station[freeRacksString]) 
    stationAvailablity += "\n"

    parsedAvailability += stationAvailablity

print(parsedAvailability)

f= open(dir_path + "../data/bilbao.csv" ,"a+")
f.write(parsedAvailability)
f.close()




