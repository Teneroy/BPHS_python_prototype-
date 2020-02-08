from threading import Thread
from imutils.video import VideoStream
from imutils.video import FPS
from Viewer import Viewer
from Viewer import viewer_t
from Viewer import data_arr_t
from TextDetect import TextDetect
from TextDetect import textdetect_t
from DistanceDetect import DistanceDetect
import time
import numpy as np
import cv2
import copy


class videomodule_t(data_arr_t, textdetect_t):
    def __init__(self, v_ob=data_arr_t(), t_ob=textdetect_t(), priority=-1, operation=-1):
        data_arr_t.__init__(self)
        textdetect_t.__init__(self)
        self.arr = v_ob.arr
        self.text = t_ob.text
        self.priority = priority
        self.operation = operation

    def setArr(self, v_arr):
        self.arr = v_arr

    def setText(self, text):
        self.text = text

    def setPriority(self, pr):
        self.priority = pr

    def setOperation(self, operation):
        self.operation = operation

    def printModData(self):
        for i in range(len(self.arr)):
            print '{object: ', self.arr[i].object, ', distance: ', self.arr[i].distance, '}'
        # print self.text
        # print self.priority
        # print self.operation


class VideoModule(Thread):
    def __init__(self, vnum=0, vnum2=1):
        Thread.__init__(self)
        self.vs = None
        self.vs2 = None
        self.view = Viewer()
        self.distance = DistanceDetect()
        self.distance.callibrationFromCamera()
        self.text = TextDetect('eng')
        self.data = videomodule_t()
        self.operation_type = 'TextReading'
        classes = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
                   "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train",
                   "tvmonitor"]
        self.view.setClasses(classes)
        self.view.setNet("C:\\BPHS_python_prototype-\\MobileNetSSD_deploy.prototxt.txt",
                         "C:\\BPHS_python_prototype-\\MobileNetSSD_deploy.caffemodel")
        self.running = True
        self.operation_type = 'ObjectDetection'
        self.videonum = vnum
        self.videonum2 = vnum2

    def setOperationType(self, operation):
        self.operation_type = operation
        if self.operation_type != 'TextReading' and self.text.focusing:
            self.text.stopFocusing()

    def getData(self):
        return self.data

    def textDetectionMode(self):
        self.data.setText(self.text.textDetect())
        #self.waitForOperation('TextReading')

    def waitForOperation(self, operation_name):
        while self.operation_type == operation_name and self.running:
            pass

    def objectDetectionMode(self, wd=600):
        COLORS = np.random.uniform(0, 255, size=(21, 3))
        print("[INFO] starting video stream...")
        time.sleep(2.0)
        #fps = FPS().start()
        data = data_arr_t()
        while self.running and self.operation_type == 'ObjectDetection':
            # grab the frame from the threaded video stream and resize it
            # to have a maximum width of 400 pixels
            frame = self.view.getFrame(self.vs, wd)
            frameR = self.view.getFrame(self.vs2, wd) # little bit weird

            # grab the frame dimensions and convert it to a blob
            (h, w) = frame.shape[:2]
            blob = self.view.convertToBlob(frame)
            # # pass the blob through the network and obtain the detections and
            # # predictions
            detections = self.view.makeDetections(blob)
            # # loop over the detections
            for i in np.arange(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with
                # the prediction
                confidence = detections[0, 0, i, 2]
                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence
                if confidence > 0.2:
                    # extract the index of the class label from the
                    # `detections`, then compute the (x, y)-coordinates of
                    # the bounding box for the object
                    idx = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    # draw the prediction on the frame
                    self.view.printPrediction(idx, confidence, frame, startX, startY, endX, endY, COLORS)
                    dist = self.distance.getDistance(frame, frameR, startX, startY, endX, endY)
                    print dist
                    data.appendElem(viewer_t(self.view.classes[idx], dist))
                    #print data.arr[0].object
                # show the output frame
                cv2.imshow("Frame", frame)
                #fps.update()
            self.data = videomodule_t(copy.deepcopy(data), textdetect_t(), 2, 0)
            data.freeArr()
            key = cv2.waitKey(20)
            if key == 27:  # exit on ESC
                break
        # stop the timer and display FPS information
        #fps.stop()
        #print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
        #print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        # do a bit of cleanup
        cv2.destroyAllWindows()

    def stop(self):
        self.running = False

    def run(self):
        print "start"
        self.vs = VideoStream(self.videonum).start()
        self.vs2 = VideoStream(self.videonum2).start()
        print self.vs
        print self.vs2
        self.view.setVideoStream(self.vs)
        self.text.setVideoStream(self.vs)
        self.text.start()
        print "text started"
        self.distance.preprocessDepthMap()
        print "start while"
        while self.running:
            print "thread iteration"
            if self.operation_type == 'TextReading':
                # change string comparing later
                self.textDetectionMode()
            elif self.operation_type == 'ObjectDetection':
                self.objectDetectionMode()
        self.vs.stop()


# ob = VideoModule()
# ob.run()

ob = VideoModule(0, 1)
ob.start()
i = 0
while True:
    time.sleep(2)
    i += 1
    ob.getData().printModData()
    print "__________________"
    # if i % 10 == 0:
    #     ob.setOperationType('TextReading')
    # if i % 20 == 0:
    #     ob.setOperationType('ObjectDetection')