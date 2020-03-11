# coding=utf-8
from threading import Thread
from VideoModule import VideoModule
from Navigation import Navigation
from Speech import SpeechClass
from PlayAudio import playTrack
import keyboard
import enum
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Commands(enum.Enum):
    NO_COMMANDS = 0
    MAKE_DIRECTION = 1



class BasicClass(Thread):
    def __init__(self):
        Thread.__init__(self)
        #self.video = VideoModule(1, 0)
        self.nav = Navigation("ru")
        self.speech = SpeechClass("ru")
        self.running = True

    def navigationSettings(self, key='', lang="en", mode="transit"):
        self.nav.setAPIkey(key)
        self.nav.setLanguage(lang)
        self.nav.setMode(mode)

    def speechSettings(self, lang="en"):
        self.speech.setLanguage(lang)

    def parseSpeechInput(self, txt):
        #txt = txt.decode('ascii')
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
        pos_start_from = txt.find('от ')
        pos_start_to = txt.find('до ')
        if pos_start_from == -1 or pos_start_to == -1:
            return '', ''
        #pos_start_from += 2
        pos_end_from = txt.find('до ') - 1
        pos_end_to = len(txt)
        _from = ''
        _to = ''
        #print len('от ')
        pos_start_to += 3
        pos_start_from += 3
        for i in range(pos_start_from, pos_end_from):
            _from += txt[i]
        for i in range(pos_start_to, pos_end_to):
            _to += txt[i]
        return _from, _to

    def run(self):
        self.navigationSettings(key="AIzaSyC7hREX7LxMCWot2qdEj31Q2D6UF-ptPH0", lang="ru")
        self.speechSettings("ru")
        #self.video.start()
        print "Video module has been started"
        playTrack('audio', 'listen.mp3')
        while self.running:
            if keyboard.get_hotkey_name() == "shift":
                aud = self.speech.record()
                txt = self.speech.recognize(aud)
                print txt
                command, result = self.parseSpeechInput(txt)
                if result['from'] != '' and result['to'] != '':
                    direction = self.nav.makeDirection(result['from'], result['to'])
                    for object_outer in direction:
                        print object_outer




ob = BasicClass()
ob.start()