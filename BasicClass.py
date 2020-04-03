# coding=utf-8
from threading import Thread
from VideoModule import VideoModule
from Navigation import Navigation
from Speech import SpeechClass
from VoiceRec import VoiceRec
from PlayAudio import playTrack
import keyboard
import enum
import sys
import json
import os

reload(sys)
sys.setdefaultencoding('utf-8')

with open('languages.json', 'r') as f:
    phrases = json.load(f)


class Commands(enum.Enum):
    NO_COMMANDS = 0
    MAKE_DIRECTION = 1


class BasicClass(Thread):
    def __init__(self):
        Thread.__init__(self)
        # self.video = VideoModule(1, 0)
        self.nav = Navigation("ru")
        self.speech = SpeechClass("ru")
        self.running = True
        # self.langfile = 'languages.json'

    def navigationSettings(self, key='', lang="en", mode="transit"):
        self.nav.setAPIkey(key)
        self.nav.setLanguage(lang)
        self.nav.setMode(mode)

    def speechSettings(self, lang="en"):
        self.speech.setLanguage(lang)

    def parseSpeechInput(self, txt):
        # txt = txt.decode('ascii')
        command = Commands.NO_COMMANDS
        if txt.find("маршрут"):
            command = Commands.MAKE_DIRECTION
            _from, _to = self.getRoute(txt)
            print _from
            print _to
            print command
            return command, {"from": _from, "to": _to}
        return command, {}

    def getRoute(self, txt):
        global phrases
        pos_start_from = txt.find(phrases["ru"]["from"])
        print pos_start_from
        pos_start_to = txt.find(phrases["ru"]["to"])
        print pos_start_to
        if pos_start_from == -1 or pos_start_to == -1:
            return '', ''
        pos_end_from = txt.find(phrases["ru"]["to"]) - 1
        pos_end_to = len(txt)
        _from = ''
        _to = ''
        pos_start_to += 3
        pos_start_from += 3
        for i in range(pos_start_from, pos_end_from):
            _from += txt[i]
        for i in range(pos_start_to, pos_end_to):
            _to += txt[i]
        return _from, _to

    def convertRouteToAudio(self, arr):
        vr = VoiceRec(language="ru")
        i = 0
        for text in arr:
            print text
            vr.textToFile(text=text, filename=('point' + str(i) + '.mp3'), folder='navfiles')
            i += 1

    def navTrackPlay(self, tnum):
        if os.path.isfile(os.getcwd() + '\\' + 'navfiles' + '\\' + 'point' + str(tnum) + '.mp3'):
            playTrack('navfiles', ('point' + str(tnum) + '.mp3'))
        else:
            print 'No file'

    def run(self):
        self.navigationSettings(key="AIzaSyC7hREX7LxMCWot2qdEj31Q2D6UF-ptPH0", lang="ru")
        self.speechSettings("ru")
        # self.video.start()
        print "Video module has been started"
        playTrack('audio', 'listen.mp3')
        numt = 0
        while self.running:
            if keyboard.get_hotkey_name() == "shift":
                aud = self.speech.record()
                txt = self.speech.recognize(aud)
                print txt
                command, result = self.parseSpeechInput(txt)
                if result['from'] != '' and result['to'] != '':
                    direction = self.nav.makeDirection(result['from'], result['to'])
                    self.convertRouteToAudio(direction)
                    numt = 0
            if keyboard.get_hotkey_name() == "ctrl":
                self.navTrackPlay(numt)
                numt += 1
            if keyboard.get_hotkey_name() == "alt":
                numt -= 1
                self.navTrackPlay(numt)


ob = BasicClass()
ob.start()
