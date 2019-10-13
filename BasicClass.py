from Viewer import Viewer

class BasicClass:

    def __init__(self):
        self.var1 = "1"
        self.var2 = "2"
        self.view = Viewer()
        classes = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
                   "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train",
                   "tvmonitor"]
        self.view.setClasses(classes)
        self.view.setNet("C:\\BPHS_python_prototype-\\MobileNetSSD_deploy.prototxt.txt", "C:\\BPHS_python_prototype-\\MobileNetSSD_deploy.caffemodel")

    def startThreads(self):
        self.view.start()
