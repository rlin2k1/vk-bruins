""" pi3_coordinates.py
This module calculates current VK-Bruin Rover Coordinates.

Author(s):
    Roy Lin

Date Created:
    October 19th, 2018
"""

# ---------------------------------------------------------------------------- #
# Import Statements for the Necessary Packages
# ---------------------------------------------------------------------------- #
import io #Input / Output
import socket #Sockets
import struct #STRUCT
import time #TIME
import picamera #Camera
import serial #Serial Connection
from  math import cos, sin, radians #Math Functions

# ---------------------------------------------------------------------------- #
# CleanUp Parameters - Initialize Coordinates to the Origin
# ---------------------------------------------------------------------------- #
pro_mini = serial.Serial('/dev/ttyUSB0', 38400)
x_init = 0.00
y_init = 0.00
x_pos = 0.00
y_pos = 0.00
t_rate = 5.00 #Receive Data Every 5 Seconds

velocity = 5.00##############

# ---------------------------------------------------------------------------- #
# Connect to Server:8000 for Connection to Computer
# ---------------------------------------------------------------------------- #
client_socket = socket.socket() #Create a New Socket
client_socket.connect(('192.168.0.111', 8124)) #Connect to the Computer
client_socket.setblocking(0) #Make Socket NON-BLOCKING
while(True):
    try:
        data = client_socket.recv(1024) #Listen for Signal
        if(data == "SEND"): #If Correct Signal
            client_socket.send(x_init + '|' + y_init) #Send Over Current X + Y
    except socket.error, e: #If EXCEPTION CAUGHT
        if ((pro_mini.inWaiting()>0) ): #Check for PRO-MINI WAIT
            yaw = pro_mini.readline() #Read the Floats
            try: #See if We Can Convert to Float
                yaw=float(yaw) #Velocity is Also Going to Be Here
            except ValueError, TypeError: #See if We Can Convert to Float
                continue #Go Past
            pos_mag = velocity * t_rate #Magnitude of Postion
            #Polar to Cartesian Conversion:
            x_pos = pos_mag * cos(radians(yaw)) + x_init
            y_pos = pos_mag * sin(radians(yaw)) + y_init
            x_init = x_pos
            y_init = y_pos