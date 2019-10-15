from __future__ import print_function
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import moxel.space
import json
import imutils
import time
import cv2

net = cv2.dnn.readNetFromCaffe("C:\\BPHS_python_prototype-\\mobilenet_deploy.prototxt", "C:\\BPHS_python_prototype-\\mobilenet.caffemodel")

with open('C:\\BPHS_python_prototype-\\labels.txt', 'r') as f:
    labels = f.readlines()
    labels = [line.replace('\n', '') for line in labels]

def predict(image):
    image.resize((224, 224))
    image = image.to_numpy_rgb()[:, :, :3].transpose(2, 0, 1)
    image = np.array(image, dtype='float32')
    image[:,:,0] -= 103.94
    image[:,:,1] -= 116.78
    image[:,:,2] -= 123.68
    image *= 0.017

    image = np.expand_dims(image, 0)
    net.blobs['data'].data[...] = image
    net.forward()
    pred = net.blobs['fc7'].data
    pred = pred.reshape(1000).tolist()
    indices = np.flip(np.argsort(pred), axis=0)

    top_pred = [(labels[x], float(pred[x])) for x in indices[:5]]

    return {
        'classes': top_pred
    }


vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()

# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    # # pass the blob through the network and obtain the detections and
    # # predictions
    net.setInput(blob)
    detections = net.forward()
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break


# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()