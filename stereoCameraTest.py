import numpy as np
import cv2
from imutils.video import VideoStream

print('Starting the Calibration. Press and maintain the space bar to exit the script\n')
print('Push (s) to save the image you want and push (c) to see next frame without saving the image')
print "Call the two cameras"
# Call the two cameras
CamR= cv2.VideoCapture(0)  # 0 -> Right Camera
print CamR
CamL= cv2.VideoCapture(1)  # 2 -> Left Camera
print CamL
while True:
    retR, frameR= CamR.read()
    retL, frameL= CamL.read()

    cv2.imshow('imgR',frameR)
    cv2.imshow('imgL',frameL)
    # End the Programme
    if cv2.waitKey(1) & 0xFF == ord(' '):   # Push the space bar and maintan to exit this Programm
        break

# Release the Cameras
CamR.release()
CamL.release()
cv2.destroyAllWindows()