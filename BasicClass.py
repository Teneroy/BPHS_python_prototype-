from Viewer import Viewer
from TextDetect import TextDetect
import time

class BasicClass:

    def __init__(self):
        self.view = Viewer()
        classes = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
                   "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train",
                   "tvmonitor"]
        self.view.setClasses(classes)
        self.view.setNet("C:\\BPHS_python_prototype-\\MobileNetSSD_deploy.prototxt.txt", "C:\\BPHS_python_prototype-\\MobileNetSSD_deploy.caffemodel")
        self.text = TextDetect('eng')

    def startThreads(self):
        self.view.start()
        time.sleep(15)
        self.view.stop()
        print "SLEEP: ", self.view.runnig
        self.view.start()
