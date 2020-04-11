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

tz = pytz.timezone('Europe/London')
now = datetime.datetime.now(tz)

url = "https://api.tfl.gov.uk/BikePoint"

r = urlopen(url)

data = r.read()
encoding = r.info().get_content_charset('utf-8')

data = json.loads(data.decode(encoding))

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
    stationName = i["commonName"]

    freeBikes   = str(i["additionalProperties"][6]['value'])
    freeDocks   = str(i["additionalProperties"][7]['value'])
    
    query = time.strftime("%Y/%m/%d %H:%M") + "," + idno + "," + stationName + "," + freeBikes + "," + freeDocks + "\n"
    
    totalQuery += query

    meas = {}
    meas["measurement"] = "bikes"
    meas["tags"] = { "station_name" : stationName, "station_id": idno}
    meas["time"] = current_time 
    meas["fields"] = { "value" : str(freeBikes) }

    json_body.append(meas)

client = InfluxDBClient('localhost', '8086', 'root', 'root', 'Bicis_London_Availability')

client.write_points(json_body)

client.close()
