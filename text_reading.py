from PIL import Image
import pytesseract
from gtts import gTTS
import os
f = open('C:\\BPHS_python_prototype-\\images\\text_photo.txt', 'w')
text = pytesseract.image_to_string(Image.open('C:\\BPHS_python_prototype-\\images\\td4.jpg'), lang='eng').encode('utf-8')
f.write(text)

text2 = "Hello"
tts = gTTS(text=text, lang='en')
tts.save("pcvoice.mp3")
os.system("start pcvoice.mp3")