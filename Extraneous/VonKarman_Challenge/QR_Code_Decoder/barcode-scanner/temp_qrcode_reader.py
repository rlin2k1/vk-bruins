import cv2 as cv
import cv2
import zbarlight
import time
from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy
#import RPi.GPIO as GPIO

# set up gpio
#GPIO.setmode(GPIO.BCM)

# initialize picamera
camera = PiCamera()
resolution = (400, 300)
camera.resolution = resolution
raw_capture = PiRGBArray(camera, size = resolution)
time.sleep(0.1)

colors = {
    "red": (0,0,255),
    "green": (0,255,0),
    "yellow": (0,255,255),
    "blue": (255,0,0)
    }

def qrCheck(arg):
    """ Check an image for a QR code, return as string """
    image_string = arg.tostring()
    try:
        code = zbarlight.qr_code_scanner(image_string, 400, 300)
        return code
    except:
        return


for frame in camera.capture_continuous(raw_capture,
                                       format = "bgr",
                                       use_video_port = True):
    # grab image as numpy array
    image = frame.array
        
    # convert image to grayscale and decode
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    decoded = qrCheck(gray)
    
    # write decoded output to frame
    cv2.putText(image, decoded, (30,30),cv2.FONT_HERSHEY_SIMPLEX,1,colors.get(decoded),2)

    # show frame
    cv2.imshow("frame", image)
    key = cv2.waitKey(60) & 0xFF
    raw_capture.truncate(0)

    # quit if q is pressed
    if key == ord('q'):
        break
cv2.destroyAllWindows()
GPIO.cleanup()
