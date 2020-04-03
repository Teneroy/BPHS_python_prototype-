# BPHS_python_prototype-
Object-oriented system that aimed on helping to blind people. System has different modules that developers can append and remove. The aim of the development of that system is to get the base for future systems in that field. Every programmer can use and upgrade this system. If you have got any questions about it, you can contact me.  

## Modules
Navigation - navigation module based on Google Maps API

Speech - speech recognition module based Google speech recognition

VoiceRec - voice recognition module based on gTTS

VideoModule - module that contains three modules, such as Viewer, TextDetect, and DistanceDetect

Viewer - module that recognize objects from video camera

TextDetect - module that recognize text from picture, person capture picture, and then google tesseract recognize text

DistanceDetect - distance detection module. Module gets data from 2 video cameras, create disparity map, and then detect distance of object in frame

## If you include VideoModule, you have to calibrate your cameras
Subprogram Take_images_for_callibration.py makes images from two cameras for camera callibration.

## Start
Install dependencies

Build and run program 
```
python main.py
```

