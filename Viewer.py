from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time
import cv2
from threading import Thread


class Viewer(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.classes = None
        self.net = None
        self.runnig = True

    def setNet(self, proto, model):
        self.net = cv2.dnn.readNetFromCaffe(proto, model)

    def setClasses(self, cl):
        self.classes = cl

    def getFrame(self, vstream, width):
        frame = vstream.read()
        frame = imutils.resize(frame, width=1000)
        return frame

    def convertToBlob(self, frame):
        return cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

    def makeDetections(self, blob):
        self.net.setInput(blob)
        return self.net.forward()

    def stop(self):
        self.runnig = False

    def printPrediction(self, index, conf, frame, sx, sy, ex, ey, colors):
        label = "{}: {:.2f}%".format(self.classes[index], conf * 100)
        cv2.rectangle(frame, (sx, sy), (ex, ey), colors[index], 2)
        y = sy - 15 if sy - 15 > 15 else sy + 15
        cv2.putText(frame, label, (sx, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[index], 2)

    #vsrc = 0, width = 600
    def startDistanceView(self, vsrc, wd):
        COLORS = np.random.uniform(0, 255, size=(len(self.classes), 3))
        print("[INFO] starting video stream...")
        vs = VideoStream(vsrc).start()
        time.sleep(2.0)
        fps = FPS().start()
        # loop over the frames from the video stream
        while self.runnig:
            #print self.runnig
            # grab the frame from the threaded video stream and resize it
            # to have a maximum width of 400 pixels
            frame = self.getFrame(vs, 600)
            # grab the frame dimensions and convert it to a blob
            (h, w) = frame.shape[:2]
            blob = self.convertToBlob(frame)
            # # pass the blob through the network and obtain the detections and
            # # predictions
            detections = self.makeDetections(blob)
            # print detections
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
                    self.printPrediction(idx, confidence, frame, startX, startY, endX, endY, COLORS)
                # show the output frame
                cv2.imshow("Frame", frame)
                fps.update()
            key = cv2.waitKey(20)
            if key == 27:  # exit on ESC
                break
        # stop the timer and display FPS information
        fps.stop()
        print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        # do a bit of cleanup
        cv2.destroyAllWindows()
        vs.stop()

    def run(self):
        self.startDistanceView(0, 600)