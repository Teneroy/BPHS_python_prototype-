# coding=utf-8
import googlemaps
from datetime import datetime
from googlemaps import geocoding
from googlemaps import directions
from googlemaps import roads
from googlemaps import elevation
from googlemaps import geolocation
import re


class Navigation:
    def __init__(self, lang="en", mode="transit", departure=datetime.now()):
        self.language = lang
        self.mode = mode
        self.departure = departure
        self.gmaps = None
        self.API = ''

    def setAPIkey(self, key):
        self.API = key
        self.gmaps = googlemaps.Client(key=self.API)

    def getCurrentLocation(self):
        geolocate_result = geolocation.geolocate(self.gmaps)
        return geolocate_result

    def setLanguage(self, lang):
        self.language = lang

    def setMode(self, mode):
        self.mode = mode

    def setDepartureTime(self, departure):
        self.departure = departure

    def makeDirection(self, dirfrom, dirto):
        if self.gmaps is None:
            return "ERROR: you have to set API key"
        directions_result = directions.directions(self.gmaps, dirfrom,
                                                  dirto,
                                                  mode=self.mode,
                                                  language=self.language,
                                                  departure_time=self.departure)
        r = directions_result[0]['legs']
        arr = r[0]['steps']
        final_res = []
        for obj in arr:
            arr_result = []
            self.parseResult(obj, arr_result)
            final_res += arr_result
            arr_result = None
        return final_res

    def parseResult(self, obj, arr_result):
        cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        cleantext = re.sub(cleanr, '', (obj['html_instructions'] + " " + obj['distance']['text']))
        arr_result.append(cleantext)
        if "steps" in obj:
            for iterob in obj['steps']:
                self.parseResult(iterob, arr_result)


# ob = Navigation("ru")
# ob.setAPIkey('AIzaSyC7hREX7LxMCWot2qdEj31Q2D6UF-ptPH0')
# res = ob.makeDirection('Брянцева, 12', 'Просвещения 33')
# for object_outer in res:
#     print object_outer


