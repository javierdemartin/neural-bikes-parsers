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
url = "http://api.citybik.es/v2/networks/citi-bike-nyc"

r = urlopen(url)

data = r.read()
encoding = r.info().get_content_charset('utf-8')

data = json.loads(data.decode(encoding))
data = data['network']['stations']

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

    idno          = str(i["id"])
    stationName = i["name"]
    freeBikes   = str(i["free_bikes"])
    freeDocks   = str(i["empty_slots"])

    meas = {}
    meas["measurement"] = "bikes"
    meas["tags"] = { "station_name" : stationName, "station_id": idno}
    meas["time"] = current_time 
    meas["fields"] = { "value" : str(freeBikes) }

    json_body.append(meas)

client = InfluxDBClient('localhost', '8086', 'root', 'root', 'Bicis_New_York_Availability')

client.write_points(json_body)

client.close()
