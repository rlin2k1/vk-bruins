""" pi1_dimension_stream_1.py
Detects Object Dimensions in Real Time Video Frames and highlights the Dimension
and outputs information based on the QR Code.

The Computer is the Server - Awaiting Images from the Raspberry Pi 1 for 
Analysis.

MOST IMPORTANT: Measuring the Number of Pixels Per a Given Metric

1. Should Be a Perfect 90 Degrees Looking Down (Birds Eye View)
2. May Be Prone to Radial / Tangential Lens Distorsion


USAGE: python pi1_dimension_stream_1.py

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

from scipy.spatial import distance as dist #Distances
from imutils import perspective #Perspective
from imutils import contours #Contours
import numpy as np #Numpy
import argparse #Argument Parser
import imutils #Imutils
import cv2 #Computer Vision Library

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
counter = 1 #Only Want 20 Pictures Max!

# ---------------------------------------------------------------------------- #
# Helper Functions for Object Dimension Analysis
# ---------------------------------------------------------------------------- #
def midpoint(ptA, ptB):
    """
    Used to define a midpoint between two sets of (x,y) coordinates
    
    Args:
        ptA (Tuple): X and Y Coordinates of Point A
        ptB (Tuple): X and Y Coordinates of Point B
    Returns:
        (Tupe): Midpoint of Point A and Point B
    """
    return( (ptA[0] + ptB[0]) * 0.5, (ptA[1]+ ptB[1]) * 0.5 )

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
        # Object Dimsionsion Detection
        # -------------------------------------------------------------------- #
        frame = np.array(image) #Make the Image into an Array formed by Numpy

        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Convert Image to
        #GRAYSCALE
        grayscale = cv2.GaussianBlur(grayscale, (7, 7), 0) #Blur the Image using
        #Gaussian Filter

        edge_detect = cv2.Canny(grayscale, 50, 100) #Edge Detection
        #Close Gaps In Between Object Edges
        edge_detect = cv2.dilate(edge_detect, None, iterations=1) #Dilation
        edge_detect = cv2.erode(edge_detect, None, iterations=1) #Erosion

        #Find the Contours that Correspond to the Objects In Our Image
        object_contours = cv2.findContours(edge_detect.copy(), \
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        object_contours = object_contours[0] if imutils.is_cv2() else \
        object_contours[1]

        #WE WILL DELETE THIS LATER
        original = frame.copy() #Make a Copy of Our Image
        pixels_per_metric = 88 #Initialize Pixels Per Metric
        # ---------------------------------------------------------------- #
        # Loop Over Each Contour Individually
        # ---------------------------------------------------------------- #
        for contour in object_contours:
        #If Contour is NOT Large, Ignore!
            if cv2.contourArea(contour) < 100:
                continue

            #Compute Bounding Box of the Contour
            #original = frame.copy() #Make a Copy of Our Image
            bounding_box = cv2.minAreaRect(contour)
            bounding_box = cv2.cv.BoxPoints(bounding_box) \
            if imutils.is_cv2() else cv2.boxPoints(bounding_box)
            bounding_box = np.array(bounding_box, dtype="int")

            #Order Points in Contour for Top Left, Top Right, Bottom Right, 
            #Bottom Left Order
            bounding_box = perspective.order_points(bounding_box)

            cv2.drawContours(original, [bounding_box.astype("int")], \
            -1, (0, 255, 0), 2) #Draw Outline of the Bounding Box in Green

            for (X, Y) in bounding_box:
                #Draw Verties in Small Red Circles
                cv2.circle(original, (int(X), int(Y)), 5, (0, 0, 255), -1)

            #Get Bounding_Box Coordinates and Midpoints
            (top_left, top_right, bottom_right, bottom_left) = bounding_box
            (tLtRX, tLtRY) = midpoint(top_left, top_right) #Midpoint Top
            #Midpoint Bottom
            (bLbRX, bLbRY) = midpoint(bottom_left, bottom_right)
            (tLbLX, tLbLY) = midpoint(top_left, bottom_left)
            (tRbRX, tRbRY) = midpoint(top_right, bottom_right)

            #Draw All Midpoints on the Circle as Blue
            cv2.circle(original, (int(tLtRX), int(tLtRY)), 5, (255, 0, 0), \
            -1)
            cv2.circle(original, (int(bLbRX), int(bLbRY)), 5, (255, 0, 0), \
            -1)
            cv2.circle(original, (int(tLbLX), int(tLbLY)), 5, (255, 0, 0), \
            -1)
            cv2.circle(original, (int(tRbRX), int(tRbRY)), 5, (255, 0, 0), \
            -1)

            #Draw Lines in Between Midpoints as Purple
            cv2.line(original, (int(tLtRX), int(tLtRY)), (int(bLbRX), \
            int(bLbRY)), (255, 0, 255), 2)
            cv2.line(original, (int(tLbLX), int(tLbLY)), (int(tRbRX), \
            int(tRbRY)), (255, 0, 255), 2)

            #Compute Euclidean Distance Between Midpoints
            object_height = dist.euclidean((tLtRX, tLtRY), (bLbRX, bLbRY))
            object_width = dist.euclidean((tLbLX, tLbLY), (tRbRX, tRbRY))
            
            #Compute Size of the Object
            object_height = object_height / pixels_per_metric
            object_width = object_width / pixels_per_metric

            #Draw Object Sizes on the Image
            cv2.putText(original, "{:.1f}in".format(object_height), \
            (int(tLtRX - 15), int(tLtRY - 10)), cv2.FONT_HERSHEY_SIMPLEX, \
            0.65, (255, 255, 255), 2)
            cv2.putText(original, "{:.1f}in".format(object_width), \
            (int(tRbRX + 10), int(tRbRY)), cv2.FONT_HERSHEY_SIMPLEX, \
            0.65, (255, 255, 255), 2)

            if( counter < 20 and \
            ( (object_height <= 3.15 and object_height >= 2.85)  and \
            (object_width <= 3.15 and object_width >= 2.85) ) ):
                cv2.imwrite('three_by_three_' + str(counter) + '.jpg', frame)
                counter = counter + 1
                three_by_three = Image.open\
                ('three_by_three_' + str(counter) + '.jpg')
                three_by_three.show() #SHOW!

        #Show Output FRAME
        cv2.imshow("Object Dimension", original)
        cv2.waitKey(1) #Press Enter for Next Object in the Image
finally:
    # ------------------------------------------------------------------------ #
    # CleanUp!
    # ------------------------------------------------------------------------ #
    connection.close() #Close that One Connection
    server_socket.close() #Close the Socket