from gtts import gTTS
import os


class VoiceRec:

    def __init__(self, language='en'):
        self.tts = gTTS(text='Initialize voice recognition', lang=language)

    def textToFile(self, text, filename, folder=''):
        self.tts.text = text.decode('utf-8')
        filepath = os.getcwd() + '\\' + folder + ('\\' if len(folder) > 0 else '') + filename
        self.tts.save(filepath)
        return filepath

    def runFile(self, filepath):
        command = "start " + filepath
        os.system(command)

    def setLang(self, lang):
        self.tts.lang = lang


# a = VoiceRec()
# file = a.textToFile("Because they were built very well")
# a.runFile(file)