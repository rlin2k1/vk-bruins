""" qr_decode_video.py
Detects QR Codes in Real Time Video Frames and highlights the QR Code
and outputs information based on the QR Code.

QR Code Scanner with ZBar

USAGE: python qr_decode_video.py

Author(s):
    Roy Lin

Date Created:
    August 28th, 2018
"""

# ---------------------------------------------------------------------------- #
# Import Statements for the Necessary Packages
# ---------------------------------------------------------------------------- #
from imutils.video import VideoStream #For Video Streaming
from pyzbar import pyzbar #ZBAR
import argparse #Argument Parser
import datetime #To Get Timing Data
import imutils #No Idea
import time #Get Time
import cv2 #Computer Vision

# ---------------------------------------------------------------------------- #
# Constructs Argument Parser for Parsing Arguments
# ---------------------------------------------------------------------------- #
argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("-o", "--output", type=str, default="qrcodes.csv", help="PATHTOOUTPUTCSVFILECONTAININGQRCODES")

arguments = vars(argument_parser.parse_args())

# ---------------------------------------------------------------------------- #
# Initialize the Video Stream
# ---------------------------------------------------------------------------- #
print("[INFO] Starting the Video Stream...")
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0) #Allows Camera to Warm Up

#Can Save QR Codes in a SQL Database, Send it to Server, Upload to Cloud, Send an Email or Text Message
csv = open(arguments["output"], "w")
found = set()

# ---------------------------------------------------------------------------- #
# Loop Over Each Frame in the Video Stream
# ---------------------------------------------------------------------------- #
while True:
    #Grab Frame from THREADED Video Stream and Resize to 400 Pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    # Find the QR Codes in the Image and Decode Each QR Code
    qrcodes = pyzbar.decode(frame)

    print("REACHED!")

    # Loop Over Detected QR Codes
    for qr_code in qrcodes:
        #Extract the Bounding Box Location of the QR Code and Draw the Bounding Box Surrounding the QR Code on the Image
        (x, y, w, h) = qr_code.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        #Need QR Decoded as a STRING
        qrData = qr_code.data.decode("utf-8")
        qrType = qr_code.type

        #Draw QR Code Data and Type on the Image
        text = "{} ({})".format(qrData, qrType)
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        #Print QR Code Type and Data to Terminal
        #Uncomment if You Don;t Want the Terminal to Be Spammed!
        print("[INFO] Found {} QR Code: {}".format(qrType, qrData))
        
        #Write TimeStamp + QR_Code to CSV (Update SET)
        if qrData not in found:
            csv.write("{},{}\n". format(datetime.datetime.now(), qrData))
            csv.flush()
            found.add(qrData)

        #Show Output FRAME
    cv2.imshow("QR Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

# ---------------------------------------------------------------------------- #
# CleanUp
# ---------------------------------------------------------------------------- #
print("[INFO] Cleaning Up...")
csv.close()
cv2.distroyAllWindows()
vs.stop()
