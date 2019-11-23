import cv2
import time

cv2.namedWindow('left_Webcam', cv2.WINDOW_NORMAL)
# cv2.namedWindow('right_Webcam', cv2.WINDOW_NORMAL)
# cv2.namedWindow('disparity', cv2.WINDOW_NORMAL)

left_frame = cv2.imread("images\\l_im.png")
right_frame = cv2.imread("C:\\BPHS_python_prototype-\\images\\r_im.png")

print left_frame

cv2.imshow('left_Webcam', left_frame)
# gray_left = cv2.cvtColor(left_frame, cv2.COLOR_BGR2GRAY)
# gray_right = cv2.cvtColor(right_frame, cv2.COLOR_BGR2GRAY)
# cv2.imshow('left_Webcam', gray_left)
# cv2.imshow('right_Webcam', gray_right)
# blockSize = 40
# stereo = cv2.StereoSGBM_create(minDisparity=1,
#     numDisparities=16,
#     blockSize=15,
#     uniquenessRatio = 10,
#     speckleWindowSize = 10,
#     speckleRange = 32,
#     disp12MaxDiff = 1,
#     P1 = 8*3*blockSize**2,
#     P2 = 32*3*blockSize**2
# )
# disparity = stereo.compute(gray_left, gray_right)
# disparity = cv2.normalize(disparity, disparity, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
# cv2.imshow('disparity', disparity)
time.sleep(100)