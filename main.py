# Created by Simon Stegmann (simon.stegmann@online-ewb.de)
# to fufill the requirements of the inteligent trash roboter
# The Script is capable of starting the TensorFlow Lite Object Detection
# and a fully functional webserver too. 
# The webseite displys the video output and is able to controll the roboters
#
# The Project was developt for TEx of the Gymnasium Höchstadt
#
# Working time ~3h (this script)

# Main script to run object detection and webserver.
import threading
import detect
import webserver
import time
import sys

def startDetectionWebserver():
    # Initialize detector
    detector = detect.ObjectDetector(camera_id=8)
    
    # Start Object Detection Thread
    detection_thread = threading.Thread(target=detector.run_detection)
    detection_thread.daemon = True
    detection_thread.start()
    
    time.sleep(0.8)
    print()
    
    # Start the WebServer Thread
    webserver_thread = webserver.WebServerThread(detector, host="0.0.0.0", port=8080)
    webserver_thread.daemon = True
    webserver_thread.start()
    
    time.sleep(0.1)
    print()
    print(f"\033[91mPress STRG+C to quit\033[0m")
    
    #print(detector.detection_result)
    #print(f"Intelligence: {webserver.intelligence}")
    #print(f"Swarm Intelligence: {webserver.swarmIntelligence}")
    
    # Keep main thread alive
    try:
        detection_thread.join()
        webserver_thread.join()
    except KeyboardInterrupt:
        print("\nShutting down...")
        detector.cleanup()
        time.sleep(0.5)
        sys.exit(0)

if __name__ == '__main__':
    startDetectionWebserver()