from gtts import gTTS
import os


class VoiceRec:

    def __init__(self):
        self.tts = gTTS(text='Initialize voice recognition', lang='en')

    def textToFile(self, text):
        self.tts.text = text
        filename = "pcvoice.mp3"
        self.tts.save(filename)
        filepath = os.getcwd() + '\\' + filename
        return filepath

    def runFile(self, filepath):
        command = "start " + filepath
        os.system(command)

    def setLang(self, lang):
        self.tts.lang = lang

# a = VoiceRec()
# file = a.textToFile("Because they were built very well")
# a.runFile(file)