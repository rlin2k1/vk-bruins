""" pi3_qr_stream_2.py
Sends Picture Frames Across the Socket to the Connected Server

The Computer is the Server - Awaiting Images from the Client(Raspberry Pi 3),

USAGE: python pi3_qr_stream_2.py

Author(s):
    Roy Lin

Date Created:
    October 3rd, 2018
"""

# ---------------------------------------------------------------------------- #
# Import Statements for the Necessary Packages
# ---------------------------------------------------------------------------- #
import io #For Input / Output
import socket #Sockets for Transferring Data from Pi to Computer
import struct #STUCT
import time #Get Time
import picamera #Library for Camera Connected to the Raspberry Pi 3

# ---------------------------------------------------------------------------- #
# Connect to Server:8000 for Connection to Computer
# ---------------------------------------------------------------------------- #
client_socket = socket.socket() #Create a New Socket
client_socket.connect(('192.168.0.111', 8000)) #Connect to the Computer

# ---------------------------------------------------------------------------- #
# After Connection, Make a File-Like Object Out of Connection
# ---------------------------------------------------------------------------- #
connection = client_socket.makefile('wb')

try:
    camera = picamera.PiCamera() #Create a New PiCamera Instance
    camera.resolution = (640, 480) #Define the Resolution of the Camera
    time.sleep(2) #Allows Camera to Warm Up

    stream = io.BytesIO() #Construct Stream to Hold Image Data

    for foo in camera.capture_continuous(stream, 'jpeg'):
        connection.write(struct.pack('<L', stream.tell())) #Write Length of
        #Capture to the Stream
        connection.flush() #Flush the Stream so It Actually Gets Sent
        stream.seek(0) #Rewind Stream
        connection.write(stream.read()) #Send Image Data Over the Socket

        stream.seek(0) #Reset the Stream for Next Capture
        stream.truncate() #Zero it Out!
    connection.write(struct.pack('<L', 0)) #Write Zero to Stream - We're Done!
finally:
    # ------------------------------------------------------------------------ #
    # CleanUp!
    # ------------------------------------------------------------------------ #
    connection.close() #Close that One Connection
    client_socket.close() #Close the Socket