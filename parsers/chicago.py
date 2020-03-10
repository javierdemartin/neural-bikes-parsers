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

tz = pytz.timezone('America/Chicago')
now = datetime.datetime.now(tz)

# URL containing the XML feed
url = "https://layer.bicyclesharing.net/map/v1/chi/map-inventory"

r = urlopen(url)

data = r.read()
encoding = r.info().get_content_charset('utf-8')

data = json.loads(data.decode(encoding))
data = data['features']

idno        = ""
stationName = ""
freeBikes   = ""
freeDocks   = ""
query       = ""
status      = ""
totalQuery  = ""

json_body = []

current_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')

for i in data: 

    #print(i)

    idno          = str(i["properties"]['station']['id'])
    stationName = i["properties"]['station']['name']
    freeBikes   = str(i['properties']['station']['bikes_available'])
    freeDocks   = str(i['properties']['station']['docks_available'])

    meas = {}
    meas["measurement"] = "bikes"
    meas["tags"] = { "station_name" : stationName, "station_id": idno}
    meas["time"] = current_time 
    meas["fields"] = { "value" : str(freeBikes) }

    json_body.append(meas)

client = InfluxDBClient('localhost', '8086', 'root', 'root', 'Bicis_Chicago_Availability')

client.write_points(json_body)

client.close()
