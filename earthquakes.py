#!/usr/bin/env python3

import json
import sys
import time
import urllib.request

f = urllib.request.urlopen('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_week.geojson')
data = json.loads(f.read())
if f.status != 200:
    print('Received status code %d while making request' % f.status)
    sys.exit(1)

for features in data['features']:
    props = features['properties']
    print('%s - %s %s' % (props['title'], time.strftime('%c', time.localtime(int(props['time']) / 1000.0)), props['url']))
