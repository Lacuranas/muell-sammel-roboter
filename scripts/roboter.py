# The Script was written without any codebase
#
# Own Work: 1h

from detect import startDetection  #Object Detection and WebServer
import detect                      #Acces of Variables
import time                        #timing and sleeping
import sys               #general System Library

if __name__ == '__main__':
  # Start the Object Detection Script
    startDetection();
    time.sleep(1)
    print("Object Detection running")
    print(detect.up)