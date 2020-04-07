# coding=utf-8
from threading import Thread
from PlayAudio import playTrack
from VoiceRec import VoiceRec
from VideoModule import videomodule_t
import copy
import os
import time
import json

fnum = 0

with open('languages.json', 'r') as f:
    phrases = json.load(f)

class Display(Thread):
    def __init__(self, lang="en"):
        Thread.__init__(self)
        self.data = None
        self.language = lang
        self.vr = VoiceRec(language=lang)
        self.display = True

    def getDisplayMode(self):
        return self.display

    def audioVisualData(self):
        global phrases
        global fnum
        if self.data.operation == 0:
            for ob in self.data.arr:
                print phrases["ru"]["classes"].get(ob.object)
                if phrases["ru"]["classes"].get(ob.object):
                    voicestring = str(phrases["ru"]["classes"][ob.object]) + ' ' + str(ob.distance) + ' м.'
                    print voicestring
                    if fnum != 0:
                        os.remove(os.getcwd() + '\\' + 'audio' + '\\' + 'situation'+str(fnum - 1)+'.mp3')
                    self.vr.textToFile(text=voicestring, filename=('situation'+str(fnum)+'.mp3'), folder='audio')
                    playTrack('audio', 'situation'+str(fnum)+'.mp3')
                    fnum += 1

    def sendData(self, data):
        self.data = copy.deepcopy(data)

    def displayMode(self, display):
        self.display = display

    def run(self):
        while True:
            if not self.display:
                continue
            temp_data = copy.deepcopy(self.data)
            if temp_data is None:
                continue
            print "Audio"
            self.audioVisualData()
            time.sleep(4)




