# Codebase from the Tensorflow Github page
#
# Changed by Simon Stegmann (simon.stegmann@online-ewb.de)
# to fufill the requirements of the inteligent trash roboter
# The Script is capable of starting the TensorFlow Lite Object Detection
# and a fully functional webserver too. 
# The webseite displys the video output and is able to controll the roboters
#
# The Project was developt for TEx of the Gymnasium Höchstadt
#
# Working time ~10h

"""Main script to run the object detection routine."""
import sys                                            #System exit
import time                                           #timing and sleeping
import threading                                      #Multithreading
import cv2                                            #Framecapturing
from tflite_support.task import core                  #Tensorflow core
from tflite_support.task import processor             #Tensorflow Image processing
from tflite_support.task import vision                #Tensorflow image
import utils                                          #Tensorflow Utils (utils.py)
from gevent.pywsgi import WSGIServer                  #Webserver
from flask import Flask, render_template, Response    #Flask Framework Webserver backend

stream = None #Save for last captured frame
up = False; #If the roboter is Moving forward / upward

app = Flask(__name__)  #initialisize flask

@app.route('/video_feed')  #Overrite route
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')  #Overrite route
def index():
    print("index")
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/startup')  #Overrite route
def startup():
    global up
    if(not up):
        up = True;
    print("up: " + str(up))
    return ""

@app.route('/stopup')  #Overrite route
def stopup():
    global up
    if(up):
        up = False;
    print("up: " + str(up))
    return ""

def run():  #start image capturing and TFlite detection Model
  # Arguments
    model = 'efficientdet_lite0.tflite'
    camera_id = 8
    width = 640
    height = 480
    num_threads = 4
    enable_edgetpu = False
  
  # Variables to calculate FPS
    counter, fps = 0, 0
    start_time = time.time()

  # Start capturing video input from the camera
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

  # Visualization parameters
    row_size = 20  # pixels
    left_margin = 24  # pixels
    text_color = (0, 0, 255)  # red
    font_size = 1
    font_thickness = 1
    fps_avg_frame_count = 10

  # Initialize the object detection model
    base_options = core.BaseOptions(
        file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)
    detection_options = processor.DetectionOptions(
        max_results=3, score_threshold=0.3)
    options = vision.ObjectDetectorOptions(
        base_options=base_options, detection_options=detection_options)
    detector = vision.ObjectDetector.create_from_options(options)
    
    while cap.isOpened():
        success, image = cap.read() # Capture frame-by-frame 
        if not success:
          sys.exit(
              'ERROR: Unable to read from webcam. Please verify your webcam settings.'
          )

        counter += 1
        image = cv2.flip(image, 1)

        # Convert the image from BGR to RGB as required by the TFLite model.
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Create a TensorImage object from the RGB image.
        input_tensor = vision.TensorImage.create_from_array(rgb_image)

        # Run object detection estimation using the model.
        detection_result = detector.detect(input_tensor)
        
        ######################
        
      # detection evaluation
      
        ######################
      
        # Draw keypoints and edges on input image
        image = utils.visualize(image, detection_result)

        # Calculate the FPS
        if counter % fps_avg_frame_count == 0:
          end_time = time.time()
          fps = fps_avg_frame_count / (end_time - start_time)
          start_time = time.time()

        # Show the FPS
        fps_text = 'FPS = {:.1f}'.format(fps)
        text_location = (left_margin, row_size)
        cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                    font_size, text_color, font_thickness)

        # Stop the program if the ESC key is pressed.
        if cv2.waitKey(1) == 27:
          break
        
        cv2.imshow('object_detector', image)
      # save image for WebServer
        save(image)
        
    cap.release()
    cv2.destroyAllWindows()
        
def gen_frames():  # read last captured frame and send to client
  # Stream to Web interface
    while True:
      # read last captured frame
        frame = read()
        success = True
        if not success:
            print("fehler")
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
          # return the converted frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

def save(image): #Save the frame
    global stream
    stream = image
    
def read(): #Return the frame
    global stream
    return stream

def startWebServer():
    #app.run(debug=False)
    #app.run(host='0.0.0.0')
  # Activate the logger of the WebServer
    #import logging
    #logging.basicConfig()
    #logger = logging.getLogger('waitress')
    #logger.setLevel(logging.DEBUG)
    
  # Start the WebServer
    from waitress import serve
    print("started Webser on Port 8080 / 80")
    serve(app, host="0.0.0.0", port=8080)
    

# Inizialisize Object Detection Thread
ObjectDetection = threading.Thread(target=run)
WebServer = threading.Thread(target=startWebServer)

# if __name__ == '__main__':
def startDetection():
  # Start Object Detection Thread
    ObjectDetection.start()
    
  # Start the WebServer Thread
    WebServer.start()
  
    # Crete iptable rules from port 80 to port 8080
    # Save the rules to file
    # activate saving of the file
    # install flask
    # install gevent