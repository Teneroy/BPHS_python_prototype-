from PIL import Image
import pytesseract
f = open('C:\\BPHS_python_prototype-\\images\\text_photo.txt', 'w')
text = pytesseract.image_to_string(Image.open('C:\\BPHS_python_prototype-\\images\\td2.jpg'), lang='eng').encode('utf-8')
print text
f.write(text)
