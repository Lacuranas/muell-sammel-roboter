# Codebase from the Tensorflow Github page
#
# Changed by Simon Stegmann (simon.stegmann@online-ewb.de)
# to fufill the requirements of the inteligent trash roboter
# The Script is capable of starting the TensorFlow Lite Object Detection 
#
# The Project was developt for TEx of the Gymnasium Höchstadt
#
# Working time ~16h

# Object detection routine
import sys
import time
import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils

class ObjectDetector:
    def __init__(self, camera_id=8, model='efficientdet_lite0.tflite'):
        self.camera_id = camera_id
        self.model = model
        self.width = 640
        self.height = 480
        self.num_threads = 4
        self.enable_edgetpu = False
        self.stream = None
        self.up = False
        self.cap = None
        self.detector = None
        self.running = False
        
    def initialize(self):
        """Initialize camera and detector."""
        # Start capturing video input from the camera
        self.cap = cv2.VideoCapture(self.camera_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        # Initialize the object detection model
        base_options = core.BaseOptions(
            file_name=self.model, use_coral=self.enable_edgetpu, num_threads=self.num_threads)
        detection_options = processor.DetectionOptions(
            max_results=3, score_threshold=0.3)
        options = vision.ObjectDetectorOptions(
            base_options=base_options, detection_options=detection_options)
        self.detector = vision.ObjectDetector.create_from_options(options)
        
        return self.cap.isOpened()

    def run_detection(self):
        """Run the main detection loop."""
        if not self.initialize():
            print("ERROR: Unable to initialize camera.")
            return

        # Variables to calculate FPS
        counter, fps = 0, 0
        start_time = time.time()
        
        # Visualization parameters
        row_size = 20  # pixels
        left_margin = 24  # pixels
        text_color = (0, 0, 255)  # red
        font_size = 1
        font_thickness = 1
        fps_avg_frame_count = 10
        
        self.running = True
        while self.running and self.cap.isOpened():
            success, image = self.cap.read()
            if not success:
                print('ERROR: Unable to read from webcam.')
                break

            counter += 1
            image = cv2.flip(image, 1)

            # Convert the image from BGR to RGB as required by the TFLite model.
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Create a TensorImage object from the RGB image.
            input_tensor = vision.TensorImage.create_from_array(rgb_image)

            # Run object detection estimation using the model.
            detection_result = self.detector.detect(input_tensor)
            
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
            self.stream = image
            
        self.cleanup()

    def cleanup(self):
        """Cleanup resources."""
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        """Get the latest frame."""
        return self.stream

    def set_up(self, value):
        """Set the up state."""
        self.up = value

    def get_up(self):
        """Get the up state."""
        return self.up