import io
import struct
from PIL import Image
from imutils.video import VideoStream #For Video Streaming
from pyzbar import pyzbar #ZBAR
import argparse #Argument Parser
import datetime #To Get Timing Data
import imutils #No Idea
import time #Get Time
import cv2 #Computer Vision
import socket #Used to send Data to Server
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np

def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("-o", "--output", type=str, default="qrcodes.csv", help="PATHTOOUTPUTCSVFILECONTAININGQRCODES")

arguments = vars(argument_parser.parse_args())

csv = open(arguments["output"], "w")

found = set()
counter = 0
while True:
    # Read the length of the image as a 32-bit unsigned int. If the length is zero, quit the loop
    image_len = struct.unpack('<L', connection.read(4))[0]
    if not image_len:
        break
    # Construct a stream to hold the image data and read the image
    # data from the connection
    image_stream = io.BytesIO()
    image_stream.write(connection.read(image_len))
    # Rewind the stream, open it as an image with PIL and do some
    # processing on it
    image_stream.seek(0)
    image = Image.open(image_stream)

    frame = np.array(image)

    frame = imutils.resize(frame, width=400)
    # Find the QR Codes in the Image and Decode Each QR Code
    qrcodes = pyzbar.decode(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    try: 
        cnts,_ = contours.sort_contours(cnts)
    except ValueError:
        counter = counter + 1
        print("ValueError Caught" + str(counter))
    else:
        pixelsPerMetric = None
        for c in cnts:
            if cv2.contourArea(c) < 100:
                continue
            orig = frame.copy()
        
            box = cv2.minAreaRect(c)
            box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
            box = np.array(box, dtype="int")
            box = perspective.order_points(box)
            cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
            for (x, y) in box:
                cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

            (tl, tr, br, bl) = box
            (tltrX, tltrY) = midpoint(tl, tr)
            (blbrX, blbrY) = midpoint(bl, br)
            (tlblX, tlblY) = midpoint(tl, bl)
            (trbrX, trbrY) = midpoint(tr, br)

            cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

            cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
            (255, 0, 255), 2)
            cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
            (255, 0, 255), 2)

            dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
            dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

            if pixelsPerMetric is None:
                pixelsPerMetric = dB / 0.955

            dimA = dA / pixelsPerMetric
            dimB = dB / pixelsPerMetric

            cv2.putText(orig, "{:.1f}in".format(dimA),
            (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
            0.65, (255, 255, 255), 2)
            cv2.putText(orig, "{:.1f}in".format(dimB),
            (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
            0.65, (255, 255, 255), 2)

            cv2.imshow("Object", orig)
            #cv2.waitKey(0)

        #print("REACHED!")

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
        #Uncomment if You Don't Want the Terminal to Be Spammed!
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