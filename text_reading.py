from PIL import Image
from gtts import gTTS
import pytesseract
import os
f = open('C:\\BPHS_python_prototype-\\images\\text_photo.txt', 'w')
text = pytesseract.image_to_string(Image.open('C:\\BPHS_python_prototype-\\images\\td1.jpg'), lang='eng').encode('utf-8')
f.write(text)
tts = gTTS(text=text, lang='en')
tts.save("pcvoice.mp3")
os.system("start pcvoice.mp3")