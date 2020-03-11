import speech_recognition as sr
import pyaudio
import numpy as np
import os
from PlayAudio import playTrack


class SpeechClass:
    def __init__(self, lang='en-US'):
        self.recogn = sr.Recognizer()
        self.language = lang

    def record(self):
        with sr.Microphone() as source:
            playTrack('audio', 'listen.mp3')
            print("Say something!")
            audio = self.recogn.listen(source)
        return audio

    def recognize(self, audio):
        try:
            text = self.recogn.recognize_google(audio, language=self.language)
            print("Google Speech Recognition thinks you said " + text)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return 'ERROR'
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return 'ERROR'

    def setLanguage(self, lang):
        self.language = lang


# ob = SpeechClass("ru")
# aud = ob.record()
# txt = ob.recognize(aud)
# print txt