""" pi1_qr_stream_1.py
Detects QR Codes in Real Time Video Frames and highlights the QR Code
and outputs information based on the QR Code.

QR Code Scanner with ZBar. The Computer is the Server - Awaiting Images from the
Raspberry Pi 1 for Analysis.

USAGE: python pi1_qr_stream_1.py

Author(s):
    Roy Lin

Date Created:
    October 3rd, 2018
"""

# ---------------------------------------------------------------------------- #
# Import Statements for the Necessary Packages
# ---------------------------------------------------------------------------- #
import io #Input / Output
import socket #Sockets for Transferring Data from Pi to Computer
import struct #STRUCT
from PIL import Image #For Image Construction

from pyzbar import pyzbar #ZBAR
import imutils #No Idea
import cv2 #Computer Vision
import numpy #Numpy

# ---------------------------------------------------------------------------- #
# Start a Socket for Listening for Connections on 0.0.0.0:8000 - All Interfaces
# ---------------------------------------------------------------------------- #
server_socket = socket.socket() #Create a New Socket
server_socket.bind(('0.0.0.0', 8000)) #Bind the IP Address and Port Together
server_socket.listen(0) #Listen on Socket

# ---------------------------------------------------------------------------- #
# Accept a Single Connection and Make a File-Like Object Out of Connection
# ---------------------------------------------------------------------------- #
connection = server_socket.accept()[0].makefile('rb') #Accept One Connection!
print("[INFO] Starting the Video Stream...")
found = set() #Do Not Want Repeat QR Codes Outputted!

# ---------------------------------------------------------------------------- #
# Loop Over Each Frame in the Video Stream
# ---------------------------------------------------------------------------- #
try:
    while True:
        # -------------------------------------------------------------------- #
        # Read the Length of the Image as 32-Bit Unsigned Int. If Length 0, Quit
        # -------------------------------------------------------------------- #
        image_len = struct.unpack('<L', \
        connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break

        image_stream = io.BytesIO() #Holds the Image Data
        image_stream.write(connection.read(image_len)) #Read and Write the Image

        image_stream.seek(0) #Rewind the Stream
        image = Image.open(image_stream) #Open the Image with PIL

        # -------------------------------------------------------------------- #
        # QR Code Detection
        # -------------------------------------------------------------------- #
        frame = numpy.array(image) #Make the Image into an Array formed by Numpy
        frame = imutils.resize(frame, width=400) #Resize to 400 Pixels

        # Find the QR Codes in the Image and Decode Each QR Code
        qrcodes = pyzbar.decode(frame)

        # Loop Over Detected QR Codes
        for qr_code in qrcodes:
            #Extract the Bounding Box Location of the QR Code and 
            #Draw the Bounding Box Surrounding the QR Code on the Image
            (x, y, w, h) = qr_code.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            #Need QR Decoded as a STRING
            qrData = qr_code.data.decode("utf-8")

            #Draw QR Code Data and Type on the Image
            text = "{} (QR Code)".format(qrData)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, \
            0.5, (0, 0, 255), 2)

            if qrData not in found:
                #Print QR Code Type and Data to Terminal
                print("[INFO] Found QR Code: {}".format(qrData))
                found.add(qrData)

        #Show Output FRAME
        cv2.imshow("QR Frame: Pi1", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
    # ------------------------------------------------------------------------ #
    # CleanUp - Part 2
    # ------------------------------------------------------------------------ #
    print("[INFO] Cleaning Up Pi1 QR Stream...")
finally:
    # ------------------------------------------------------------------------ #
    # CleanUp - Part 2
    # ------------------------------------------------------------------------ #
    connection.close() #Close that One Connection
    server_socket.close() #Close the Socket