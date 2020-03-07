# coding=utf-8
import responses

import googlemaps
from datetime import datetime
from googlemaps import geocoding
from googlemaps import directions
from googlemaps import roads
from googlemaps import elevation
from googlemaps import geolocation
import json


def printWay(obj):
    print obj['html_instructions'] + " " + obj['distance']['text']
    #print obj
    if "steps" in obj:
        for iterob in obj['steps']:
            printWay(iterob)
    else:
        return


gmaps = googlemaps.Client(key='')
geocode_result = geocoding.geocode(gmaps, '1600 Amphitheatre Parkway, Mountain View, CA')
print geocode_result
# Look up an address with reverse geocoding
#reverse_geocode_result = geocoding.reverse_geocode(gmaps, geocode_result)
#print reverse_geocode_result
# Request directions via public transit
now = datetime.now()
directions_result = directions.directions(gmaps, "Брянцева, 12",
                                     "Учительская ул., 12",
                                     mode="transit",
                                     language="ru",
                                     departure_time=now)
print directions_result[0]
print directions_result[0].items()[6]

for ob in directions_result[0].items():
    print ob

res = directions_result[0].items()[6]
#print res[1][0]['steps']

arr = res[1][0]['steps']
for ob in arr:
    printWay(ob)


geolocate_result = geolocation.geolocate(gmaps)
print geolocate_result