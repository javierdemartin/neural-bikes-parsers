#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################
### Javier de Martin - 2017 ###
###############################

from influxdb import InfluxDBClient

import xml.etree.ElementTree as ET
from urllib.request import urlopen
import string
import time
import os
import datetime
import re
import collections
import codecs
import json


import pytz

dir_path = os.path.dirname(os.path.realpath(__file__))

tz = pytz.timezone('America/New_York')
now = datetime.datetime.now(tz)

# URL containing the XML feed
url = "https://gbfs.citibikenyc.com/gbfs/en/station_information.json"

station_status_url = "https://gbfs.citibikenyc.com/gbfs/en/station_status.json"

r = urlopen(url)

data = r.read()
encoding = r.info().get_content_charset('utf-8')


data = json.loads(data.decode(encoding))
data = data['data']['stations']

# Dict data
##################

stations_dict = {}

for i in data: 
	stations_dict[i['station_id']] = i['name']

r = urlopen(station_status_url)

data = r.read()
encoding = r.info().get_content_charset('utf-8')

station_status_data = json.loads(data.decode(encoding))
station_status_data = station_status_data['data']['stations']


idno        = ""
stationName = ""
freeBikes   = ""
freeDocks   = ""
query       = ""
status      = ""
totalQuery  = ""

json_body = []

current_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')

for i in station_status_data: 

    idno          = str(i["station_id"])
    stationName = stations_dict[idno] # i["name"]
    freeBikes   = str(i["num_bikes_available"])
    freeDocks   = str(i["num_docks_available"])

    meas = {}
    meas["measurement"] = "bikes"
    meas["tags"] = { "station_name" : stationName, "station_id": idno}
    meas["time"] = current_time 
    meas["fields"] = { "value" : str(freeBikes) }

    json_body.append(meas)
    
print(json_body)

client = InfluxDBClient('localhost', '8086', 'root', 'root', 'Bicis_New_York_Availability')

client.write_points(json_body)

client.close()
