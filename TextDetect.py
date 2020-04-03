import cv2
from imutils.video import VideoStream
from VoiceRec import VoiceRec
from threading import Thread
from PIL import Image
import pytesseract


class TextDetect(Thread):
    def __init__(self, ln):
        Thread.__init__(self)
        self.lang = ln
        self.voice = VoiceRec()
        self.voice.setLang('en' if self.lang == 'eng' else self.lang)
        self.vs = None
        self.threadrun = False
        self.focusing = False

    def setVideoStream(self, vs):
        self.vs = vs

    def stopFocusing(self):
        self.focusing = False

    def stop(self):
        self.threadrun = False

    def takePicture(self):
        self.focusing = True
        while self.focusing:
            frame = self.vs.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            fm = cv2.Laplacian(gray, cv2.CV_64F).var()
            # Sample quality bar. Parameters adjusted manually to fit horizontal image size
            cv2.rectangle(frame, (0, 1080), (int(fm * 1.6), 1040), (0, 0, 255), thickness=cv2.FILLED)
            im = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
            cv2.imshow("Output", im)
            k = cv2.waitKey(1) & 0xff
            #print fm
            #if fm < 50.0:
            if k == ord('s'):
                break
        filename = "saved_img.jpg"
        cv2.imwrite(filename, frame)
        return filename

    def readText(self, filename):
        return pytesseract.image_to_string(Image.open('C:\\BPHS_python_prototype-\\' + filename), lang=self.lang).encode('utf-8')

    def textDetect(self):
        filename = self.takePicture()
        if filename == '':
            return ''
        # print filename
        text = self.readText(filename)
        # print text
        # filepath = self.voice.textToFile(text)
        # self.voice.runFile(filepath)
        return text

    def voiceText(self, text):
        filepath = self.voice.textToFile(text=text, filename='pcvoice.mp3')
        print filepath
        self.voice.runFile(filepath)

    def run(self):
        self.threadrun = True
        while self.threadrun:
            pass

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
