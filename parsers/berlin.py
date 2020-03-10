#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################
### Javier de Martin - 2017 ###
###############################

from influxdb import InfluxDBClient

import xml.etree.ElementTree as ET
from urllib.request import urlopen
import urllib
import string
import re
import time
import os
import datetime
import re
import collections
import codecs
import json

dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"

# URL containing the XML feed
url = "https://api.nextbike.net/maps/nextbike-live.json?city=362"

#iresponse = urllib.request.urlopen(url)
req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
con = urllib.request.urlopen(req)

#r = urllib.request.urlopen(url)

data = con.read()

encoding = con.info().get_content_charset('utf-8')

import requests

data = requests.get(url).json()  #json.loads(data.decode(encoding))
data = data["countries"][0]["cities"][0]["places"]


# Get current weekday
weekno = -1
weekday = ""
weekdays = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
weekno = datetime.datetime.today().weekday()
weekday = weekdays[weekno]

idno        = ""
stationName = ""
freeBikes   = ""
freeDocks   = ""
query       = ""
totalQuery  = ""

json_body = []

current_time = time.strftime('%Y-%m-%dT%H:%M:%SZ',time.localtime(time.time()))

for i in data: 
    
    idno          = str(i["uid"])

    stationName = i["name"] #.split("-")[1]
    freeBikes   = str(i["bikes"])
    freeDocks   = str(i["free_racks"])

    if bool(re.match("BIKE \d{1,}",stationName)): continue 
    
    query = time.strftime("%Y/%m/%d %H:%M") + "," + weekday + "," + idno + "," + stationName + "," + freeBikes + "," + freeDocks + "\n"
    
    totalQuery += query

    meas = {}
    meas["measurement"] = "bikes"
    meas["tags"] = { "station_name" : stationName, "station_id": idno}
    meas["time"] = current_time 
    meas["fields"] = { "value" : str(freeBikes) }

    json_body.append(meas)

with codecs.open(dir_path + "../data/berlin.csv", "a", "utf8") as file:
   file.write(totalQuery)

client = InfluxDBClient('localhost', '8086', 'root', 'root', 'Bicis_Berlin_Availability')

client.write_points(json_body)

client.close()

