# Changed by Simon Stegmann (simon.stegmann@online-ewb.de)
# To fufill the requirements of the inteligent trash roboter
# The script is a fully functional webserver. 
# The webseite displys the video output and is able to controll the roboters
#
# The Project was developt for TEx of the Gymnasium Höchstadt
#
# Working time ~8h (this script)
# Version: 1.0

import cv2
from flask import Flask, render_template, Response, jsonify
from waitress import serve
import threading

#Flask Framework
app = Flask(__name__)

#Detector for image frames
detector = None

#Manual controll
manualUp = False
manualDown = False
manualRight = False
manualLeft = False

# intelligence settings
intelligence = True
swarmIntelligence = True

#Define Routes for Webseite Requests
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/up/start')
def up_start():
    global manualUp
    manualUp = True
    return "success"

@app.route('/up/stop')
def up_stop():
    global manualUp
    manualUp = False
    return "success"

@app.route('/down/start')
def down_start():
    global manualDown
    manualDown = True
    return "success"

@app.route('/down/stop')
def down_stop():
    global manualDown
    manualDown = False
    return "success"

@app.route('/left/start')
def left_start():
    global manualLeft
    manualLeft = True
    return "success"

@app.route('/left/stop')
def left_stop():
    global manualLeft
    manualLeft = False
    return "success"

@app.route('/right/start')
def right_start():
    global manualRight
    manualRight = True
    return "success"

@app.route('/right/stop')
def right_stop():
    global manualRight
    manualRight = False
    return "success"

@app.route('/intelligence/<type>/<value>')
def set_intelligence(type, value):
    global intelligence, swarmIntelligence
    
    bool_value = value.lower() == 'true'
    
    if type == 'intelligence':
        intelligence = bool_value
        print(f"Intelligence set to: {intelligence}")
        
        # If deactivating intelligance, deactivate swarmintelligence too
        if not intelligence:
            swarmIntelligence = False
            print(f"Swarm Intelligence set to: {swarmIntelligence}")
    
    elif type == 'swarmintelligence':
        swarmIntelligence = bool_value
        print(f"Swarm Intelligence set to: {swarmIntelligence}")

    return "success"

@app.route('/get_intelligence_status')
def get_intelligence_status():
    """Gibt den aktuellen Status der Intelligenz-Einstellungen zurück."""
    return jsonify({
        'intelligence': intelligence,
        'swarmIntelligence': swarmIntelligence
    })

#Generate Frames to show in the Live View
def gen_frames():
    while True:
        if detector:
            frame = detector.get_frame()
            if frame is not None:
                ret, buffer = cv2.imencode('.jpg', frame)
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + 
                           buffer.tobytes() + b'\r\n')

def start_webserver(detector_instance, on_restart=None, host="0.0.0.0", port=8080):
    global detector, restart_callback
    detector = detector_instance
    restart_callback = on_restart
    print(f"Started Webserver on {host}:{port}")
    print(f"Accessible via http://localhost:{port}")
    serve(app, host=host, port=port)

class WebServerThread(threading.Thread):
    def __init__(self, detector_instance, on_restart=None, host="0.0.0.0", port=8080):
        super().__init__()
        self.detector = detector_instance
        self.on_restart = on_restart
        self.host = host
        self.port = port
        self.daemon = True
        
    def run(self):
        start_webserver(self.detector, self.on_restart, self.host, self.port)
