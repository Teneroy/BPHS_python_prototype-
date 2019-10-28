from PIL import Image
import pytesseract
from gtts import gTTS
import os
f = open('C:\\BPHS_python_prototype-\\images\\text_photo.txt', 'w')
text = pytesseract.image_to_string(Image.open('C:\\BPHS_python_prototype-\\images\\td1.jpg'), lang='eng').encode('utf-8')
f.write(text)

text2 = "Hello"
tts = gTTS(text=text2, lang='en')
tts.save("pcvoice.mp3")
os.system("start pcvoice.mp3")
i = 0
while True:
    i += 1
    if i == 10000000:
        break
tts.text = text
tts.save("pcvoice2.mp3")
os.system("start pcvoice2.mp3")
print os.getcwd()