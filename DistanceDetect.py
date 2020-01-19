import numpy as np
import cv2
#from openpyxl import Workbook  # Used for writing data into an Excel file
from sklearn.preprocessing import normalize
from threading import Thread


class DistanceDetect(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.criteria_stereo = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # Prepare object points
        self.objp = np.zeros((9 * 6, 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)
        # Arrays to store object points and image points from all images
        self.objpoints = []  # 3d points in real world space
        self.imgpointsR = []  # 2d points in image plane
        self.imgpointsL = []
        self.ChessImaR = None
        self.ChessImaL = None
        self.kernel = np.ones((3, 3), np.uint8)

    def coords_mouse_disp(event, x, y, flags, param, disp): #private
        if event == cv2.EVENT_LBUTTONDBLCLK:
            average = 0
            for u in range(-1, 2):
                for v in range(-1, 2):
                    average += disp[y + u, x + v]
            average = average / 9
            Distance = -593.97 * average ** (3) + 1506.8 * average ** (2) - 1373.1 * average + 522.06
            Distance = np.around(Distance * 0.01, decimals=2)
            print('Distance: ' + str(Distance) + ' m')

    def callibrationFromCamera(self): #public
        # Start calibration from the camera
        print('Starting calibration for the 2 cameras... ')
        # Call all saved images
        for i in range(0,
                       53):  # Put the amount of pictures you have taken for the calibration inbetween range(0,?) wenn starting from the image number 0
            t = str(i)
            print t
            ChessImaR = cv2.imread('chessboard-R' + t + '.png', 0)  # Right side
            ChessImaL = cv2.imread('chessboard-L' + t + '.png', 0)  # Left side
            retR, cornersR = cv2.findChessboardCorners(ChessImaR,
                                                       (9, 6),
                                                       None)  # Define the number of chees corners we are looking for
            retL, cornersL = cv2.findChessboardCorners(ChessImaL,
                                                       (9, 6), None)  # Left side
            if (True == retR) & (True == retL):
                self.objpoints.append(self.objp)
                cv2.cornerSubPix(ChessImaR, cornersR, (11, 11), (-1, -1), self.criteria)
                cv2.cornerSubPix(ChessImaL, cornersL, (11, 11), (-1, -1), self.criteria)
                self.imgpointsR.append(cornersR)
                self.imgpointsL.append(cornersL)

    def determinateCameraParams(self, objpoints, imgpoints, ChessIma): #private
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints,
                                                                imgpoints,
                                                                ChessIma.shape[::-1], None, None)
        h, w = ChessIma.shape[:2]
        Omtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist,
                                                    (w, h), 1, (w, h))
        return ret, mtx, dist, rvecs, tvecs, Omtx, roi

    def calibrateCameraForStereo(self, objpoints, imgpointsL, imgpointsR, mtxL, distL, mtxR, distR, ChessImaR, criteria_stereo):
        # StereoCalibrate function
        flags = 0
        flags |= cv2.CALIB_FIX_INTRINSIC
        retS, MLS, dLS, MRS, dRS, R, T, E, F = cv2.stereoCalibrate(objpoints,
                                                                   imgpointsL,
                                                                   imgpointsR,
                                                                   mtxL,
                                                                   distL,
                                                                   mtxR,
                                                                   distR,
                                                                   ChessImaR.shape[::-1],
                                                                   criteria_stereo,
                                                                   flags)
        # StereoRectify function
        rectify_scale = 0  # if 0 image croped, if 1 image nor croped
        RL, RR, PL, PR, Q, roiL, roiR = cv2.stereoRectify(MLS, dLS, MRS, dRS,
                                                          ChessImaR.shape[::-1], R, T,
                                                          rectify_scale,
                                                          (0,
                                                           0))  # last paramater is alpha, if 0= croped, if 1= not croped
        # initUndistortRectifyMap function
        Left_Stereo_Map = cv2.initUndistortRectifyMap(MLS, dLS, RL, PL,
                                                      ChessImaR.shape[::-1],
                                                      cv2.CV_16SC2)  # cv2.CV_16SC2 this format enables us the programme to work faster
        Right_Stereo_Map = cv2.initUndistortRectifyMap(MRS, dRS, RR, PR,
                                                       ChessImaR.shape[::-1], cv2.CV_16SC2)
        return Left_Stereo_Map, Right_Stereo_Map

    def createStereoSGBM(self, window_size, min_disp):
        stereo = cv2.StereoSGBM_create(minDisparity=min_disp,
                                       numDisparities=num_disp,
                                       blockSize=window_size,
                                       uniquenessRatio=10,
                                       speckleWindowSize=100,
                                       speckleRange=32,
                                       disp12MaxDiff=5,
                                       P1=8 * 3 * window_size ** 2,
                                       P2=32 * 3 * window_size ** 2)
        # Used for the filtered image
        stereoR = cv2.ximgproc.createRightMatcher(stereo)  # Create another stereo for right this time
        return stereo, stereoR

    def setFilterParams(self, lmbda, sigma, stereo):
        visual_multiplier = 1.0
        wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=stereo)
        wls_filter.setLambda(lmbda)
        wls_filter.setSigmaColor(sigma)
        return wls_filter

    def makeDepthMap(self, frameL, frameR, Left_Stereo_Map, Right_Stereo_Map, stereo, stereoR, wls_filter, min_disp, num_disp, kernel): #privates
        # Rectify the images on rotation and alignement
        Left_nice = cv2.remap(frameL, Left_Stereo_Map[0], Left_Stereo_Map[1], cv2.INTER_LANCZOS4,
                              cv2.BORDER_CONSTANT,
                              0)  # Rectify the image using the kalibration parameters founds during the initialisation
        Right_nice = cv2.remap(frameR, Right_Stereo_Map[0], Right_Stereo_Map[1], cv2.INTER_LANCZOS4,
                               cv2.BORDER_CONSTANT, 0)

        # Show the Undistorted images
        # cv2.imshow('Both Images', np.hstack([Left_nice, Right_nice]))
        # cv2.imshow('Normal', np.hstack([frameL, frameR]))

        # Convert from color(BGR) to gray
        grayR = cv2.cvtColor(Right_nice, cv2.COLOR_BGR2GRAY)
        grayL = cv2.cvtColor(Left_nice, cv2.COLOR_BGR2GRAY)

        # Compute the 2 images for the Depth_image
        disp = stereo.compute(grayL, grayR)  # .astype(np.float32)/ 16
        dispL = disp
        dispR = stereoR.compute(grayR, grayL)
        dispL = np.int16(dispL)
        dispR = np.int16(dispR)

        # Using the WLS filter
        filteredImg = wls_filter.filter(dispL, grayL, None, dispR)
        filteredImg = cv2.normalize(src=filteredImg, dst=filteredImg, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX);
        filteredImg = np.uint8(filteredImg)
        # cv2.imshow('Disparity Map', filteredImg)
        disp = ((disp.astype(
            np.float32) / 16) - min_disp) / num_disp  # Calculation allowing us to have 0 for the most distant object able to detect

        ##    # Resize the image for faster executions
        ##    dispR= cv2.resize(disp,None,fx=0.7, fy=0.7, interpolation = cv2.INTER_AREA)
        # Filtering the Results with a closing filter
        closing = cv2.morphologyEx(disp, cv2.MORPH_CLOSE,
                                   kernel)  # Apply an morphological filter for closing little "black" holes in the picture(Remove noise)

        # Colors map
        dispc = (closing - closing.min()) * 255
        dispC = dispc.astype(
            np.uint8)  # Convert the type of the matrix from float32 to uint8, this way you can show the results with the function cv2.imshow()
        disp_Color = cv2.applyColorMap(dispC,
                                       cv2.COLORMAP_OCEAN)  # Change the Color of the Picture into an Ocean Color_Map
        filt_Color = cv2.applyColorMap(filteredImg, cv2.COLORMAP_OCEAN)

        # Show the result for the Depth_image
        # cv2.imshow('Disparity', disp)
        # cv2.imshow('Closing',closing)
        # cv2.imshow('Color Depth',disp_Color)
        cv2.imshow('Filtered Color Depth', filt_Color)
        return disp

    def calculateRectangleDistance(self, disp): #private
        average = 0
        # for u in range(-1, 2):
        #     for v in range(-1, 2):
        #         average += disp[y + u, x + v]
        temp = []
        for i in range(len(disp)):
            for j in range(len(disp[i])):
                temp.append(disp[i][j])
        average = temp[round(len(temp) / 2.0)]
        average = average / 9
        Distance = -593.97 * average ** (3) + 1506.8 * average ** (2) - 1373.1 * average + 522.06
        Distance = np.around(Distance * 0.01, decimals=2)
        print('Distance: ' + str(Distance) + ' m')
        return Distance

    def getDistance(self): #public
        dispar = self.makeDepthMap()
        return self.getDistance(dispar)


    def run(self):
        print('Cameras Ready to use')

        # Create StereoSGBM and prepare all parameters
        window_size = 3
        min_disp = 2
        num_disp = 130 - min_disp

        # Call the two cameras
        CamR = cv2.VideoCapture(1)  # Wenn 0 then Right Cam and wenn 2 Left Cam
        CamL = cv2.VideoCapture(2)
        # kernel = np.ones((3, 3), np.uint8)
        while True:
            # Start Reading Camera images
            retR, frameR = CamR.read()
            retL, frameL = CamL.read()

            # Mouse click
            print self.getDistance()

            # End the Programme
            if cv2.waitKey(1) & 0xFF == ord(' '):
                break

        # Save excel
        ##wb.save("data4.xlsx")

        # Release the Cameras
        CamR.release()
        CamL.release()
        cv2.destroyAllWindows()