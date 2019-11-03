from threading import Thread
from imutils.video import VideoStream
from Viewer import Viewer
from TextDetect import TextDetect
import time


class VideoModule(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.vs = None
        self.view = Viewer()
        classes = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
                   "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train",
                   "tvmonitor"]
        self.view.setClasses(classes)
        self.view.setNet("C:\\BPHS_python_prototype-\\MobileNetSSD_deploy.prototxt.txt",
                         "C:\\BPHS_python_prototype-\\MobileNetSSD_deploy.caffemodel")
        self.text = TextDetect('eng')
        #self.running = True

    def run(self):
        vs = VideoStream(0).start()
        self.view.setVideoStream(vs)
        self.text.setVideoStream(vs)
        self.view.startDistanceView(600)
        time.sleep(10)
        self.view.stop()
        self.text.startTextDetection()
        vs.stop()


ob = VideoModule()
ob.run()
