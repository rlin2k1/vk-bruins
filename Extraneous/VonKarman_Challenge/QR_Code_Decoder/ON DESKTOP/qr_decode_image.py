""" qr_decode_image.py
Takes in a single image (PNG) as an argument and highlights the QR Code
and outputs information based on the QR Code.

QR Code Scanner with ZBar

USAGE: python qr_decode_image.py --image image.png

Author(s):
    Roy Lin

Date Created:
    August 28th, 2018
"""

# ---------------------------------------------------------------------------- #
# Import Statements for the Necessary Packages
# ---------------------------------------------------------------------------- #
from pyzbar import pyzbar #ZBAR
import argparse #Argument Parser
import cv2 #Computer Vision Library

# ---------------------------------------------------------------------------- #
# Constructs Argument Parser for Parsing Arguments
# ---------------------------------------------------------------------------- #
argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("-i", "--image", required=True, help="PATHTOINPUTIMAGE")

arguments = vars(argument_parser.parse_args())

# ---------------------------------------------------------------------------- #
# Load the Imputted Image from Command Line
# ---------------------------------------------------------------------------- #
image = cv2.imread(arguments["image"])

# ---------------------------------------------------------------------------- #
# Find the QR Codes in the Image and Decode Each QR Code
# ---------------------------------------------------------------------------- #
qrcodes = pyzbar.decode(image)

# ---------------------------------------------------------------------------- #
# Loop Over Detected QR Codes
# ---------------------------------------------------------------------------- #
for qr_code in qrcodes:
    #Extract the Bounding Box Location of the QR Code and Draw the Bounding Box Surrounding the QR Code on the Image
    (x, y, w, h) = qr_code.rect
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    #Need QR Decoded as a STRING
    qrData = qr_code.data.decode("utf-8")
    qrType = qr_code.type

    #Draw QR Code Data and Type on the Image
    text = "{} ({})".format(qrData, qrType)
    cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    #Print QR Code Type and Data to Terminal
    print("[INFO] Found {} QR Code: {}".format(qrType, qrData))

#Show Output Image
cv2.imshow("QR Image", image)
cv2.waitKey(0)