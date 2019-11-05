import cv2
from imutils.video import VideoStream
from VoiceRec import VoiceRec
#from threading import Thread
from PIL import Image
import pytesseract


class textdetect_t:
    def __init__(self, text=''):
        self.text = text


class TextDetect:
    def __init__(self, ln):
        #Thread.__init__(self)
        self.lang = ln
        self.voice = VoiceRec()
        self.voice.setLang('en' if self.lang == 'eng' else self.lang)
        self.vs = None

    def setVideoStream(self, vs):
        self.vs = vs

    def takePicture(self):
        while True:
            frame = self.vs.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            fm = cv2.Laplacian(gray, cv2.CV_64F).var()
            # Sample quality bar. Parameters adjusted manually to fit horizontal image size
            cv2.rectangle(frame, (0, 1080), (int(fm * 1.6), 1040), (0, 0, 255), thickness=cv2.FILLED)
            im = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
            cv2.imshow("Output", im)
            k = cv2.waitKey(1) & 0xff
            print fm
            if fm < 50.0:
                break
        filename = "saved_img.jpg"
        cv2.imwrite(filename, frame)
        return filename

    def readText(self, filename):
        return pytesseract.image_to_string(Image.open('C:\\BPHS_python_prototype-\\' + filename), lang=self.lang).encode('utf-8')

    def detectText(self):
        filename = self.takePicture()
        #print filename
        text = self.readText(filename)
        #print text
        # filepath = self.voice.textToFile(text)
        # self.voice.runFile(filepath)
        return text


# ob = TextDetect('eng')
# ob.start()

#print pytesseract.image_to_string(Image.open('C:\\BPHS_python_prototype-\\saved_img.jpg'), lang='eng').encode('utf-8')

# cap = VideoStream(0).start()
#
# while True:
#     frame = cap.read()
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     fm = cv2.Laplacian(gray, cv2.CV_64F).var()
#     # Sample quality bar. Parameters adjusted manually to fit horizontal image size
#     cv2.rectangle(frame, (0, 1080), (int(fm*1.6), 1040), (0,0,255), thickness=cv2.FILLED)
#     im = cv2.resize(frame, None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
#     cv2.imshow("Output", im)
#     print fm
#     k = cv2.waitKey(1) & 0xff
#     if fm > 220.0:
#         break
# cv2.imwrite("saved_img.jpg", frame)
