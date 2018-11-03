""" pi3_qr_stream_1.py
Detects QR Codes in Real Time Video Frames and highlights the QR Code
and outputs information based on the QR Code.

QR Code Scanner with ZBar. The Computer is the Server - Awaiting Images from the
Raspberry Pi 3 for Analysis.

USAGE: python pi3_qr_stream_1.py

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
import matplotlib.pyplot as plt #For Terrain Mapping

# ---------------------------------------------------------------------------- #
# Start a Socket for Listening for Connections on 0.0.0.0:8000 - All Interfaces
# ---------------------------------------------------------------------------- #
server_socket = socket.socket() #Create a New Socket
server_socket.bind(('0.0.0.0', 8000)) #Bind the IP Address and Port Together
server_socket.listen(0) #Listen on Socket

# ---------------------------------------------------------------------------- #
# Start a Socket for Listening for Connections on 0.0.0.0:8123 - All Interfaces
# ---------------------------------------------------------------------------- #
server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #CreateSocket
server_socket2.bind(('0.0.0.0',8123)) #Bind the IP Address and Port Together
server_socket2.listen(1) #Listen on Socket

# ---------------------------------------------------------------------------- #
# Accept a Single Connection and Make a File-Like Object Out of Connection
# ---------------------------------------------------------------------------- #
connection = server_socket.accept()[0].makefile('rb') #Accept One Connection!
connection2, address = server_socket2.accept()
print("[INFO] Starting the Video Stream...")
found = set() #Do Not Want Repeat QR Codes Outputted!
list_x_coordinates = [0] #X Coordinates
list_y_coordinates = [0] #Y Coordinates
list_qrCodes = [(0, 0, 0)] #QR Code Words

# ---------------------------------------------------------------------------- #
# Helper Function for Raspberry Pi3 - QR Stream
# ---------------------------------------------------------------------------- #
def RepresentsInt(qrData):
    """
    Checks if the Given String Represents an Integer.
    
    Args:
        qrData (String): String of the QR Code Representation.
    Returns:
        (Bool): True if String Can Be TypeCasted to an Integer. False Otherwise.
    """
    try: 
        int(qrData) #Try to TypeCast String to Integer
        return True
    except ValueError:
        return False

def return_coordinate():
    """
    Sends a Request for Raspberry Pi to Send Over Current Location Coordinates.
    
    Args:
        none (Void): NULL.
    Returns:
        (List): List of X and Y Coordinates of the Current Position.
    """
    connection2.send("SEND") #Signal Message
    data = connection2.recv(1024) #Get Coordinates
    return data.split('|') #Split into X and Y Coordinates

def map_coordinates(list_x_coordinates, list_y_coordinates, list_qrCodes):
    """
    Creates a Plot of the Coordinates and QR Code Representations.
    
    Args:
        list_x_coordinates (List): List of X Coordinates of the Corresponding
        QR codes.
        list_y_coordinates (List): List of Y Coordinates of the Corresponding
        QR Codes
        list_qrCodes (List): List of the QR Code Representations along with X/Y
        Coordinates
    Returns:
        (NULL): Shows and Saves the Terrain Map
    """
    fig, ax = plt.subplots() #Create a Terrain Map
    ax.scatter(list_x_coordinates, list_y_coordinates) #Scatter Plot the X + Y
    for i, txt in enumerate(list_qrCodes): #Through Each QR Code
        ax.annotate(txt[0], (list_x_coordinates[i], list_y_coordinates[i]), \
        xytext=(list_x_coordinates[i] + 3 , list_y_coordinates[i] + 3), \
        fontsize = 20) #Text
    #Begin to Draw Arrows
    list_qrCodes = sorted(list_qrCodes, key=lambda x: x[0])
    for i in range(0, len(list_qrCodes) - 1):
        plt.arrow(list_qrCodes[i][1], list_qrCodes[i][2], \
        list_qrCodes[i + 1][1] - list_qrCodes[i][1], \
        list_qrCodes[i + 1][2] - list_qrCodes[i][2], head_width=5, \
        head_length=5, fc='yellow', ec='black', length_includes_head = True)
    plt.savefig('qr_map.png', bbox_inches="tight") #Show Everything
    qr_map = Image.open('qr_map.png') #Open Image
    qr_map.show() #SHOW!

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

            if (qrData not in found):
                #Print QR Code Type and Data to Terminal
                print("[INFO] Found QR Code: {}".format(qrData))
                found.add(qrData)
                if(RepresentsInt(qrData)):
                    #ADD COORDINATE WITH THE QR DATA
                    coordinate = return_coordinate()
                    list_qrCodes.append( (qrData, coordinate[0], coordinate[1]) )
                    list_x_coordinates.append(coordinate[0])
                    list_y_coordinates.append(coordinate[1])
        #Show Output FRAME
        cv2.imshow("QR Frame: Pi3", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
    # ------------------------------------------------------------------------ #
    # CleanUp - Part 2
    # ------------------------------------------------------------------------ #
    print("[INFO] Cleaning Up Pi3 QR Stream...")
    map_coordinates(list_x_coordinates, list_y_coordinates, list_qrCodes)
finally:
    # ------------------------------------------------------------------------ #
    # CleanUp - Part 2
    # ------------------------------------------------------------------------ #
    connection.close() #Close that One Connection
    server_socket.close() #Close the Socket