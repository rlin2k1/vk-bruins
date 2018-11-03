""" size_cv.py
Detects Objects in Real Time Video Frames and Highlights the Object Dimensions
and Outputs Information based on the Object Dimensions.

Object Dimensions Analyzer

USAGE: python size_cv.py

Author(s):
    Roy Lin

Date Created:
    September 28th, 2018
"""
# ---------------------------------------------------------------------------- #
# Import Statements for the Necessary Packages
# ---------------------------------------------------------------------------- #
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

# ---------------------------------------------------------------------------- #
# Midpoint Formula
# ---------------------------------------------------------------------------- #
def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

# ---------------------------------------------------------------------------- #
# Constructs Argument Parser for Parsing Arguments
# ---------------------------------------------------------------------------- #
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
ap.add_argument("-w", "--width", type=float, required=True, help="width of the left-most object in the image (in inches)")
args = vars(ap.parse_args())

# ---------------------------------------------------------------------------- #
# Load the Image, Convert to Grayscale, Blur
# ---------------------------------------------------------------------------- #
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)

# ---------------------------------------------------------------------------- #
# Perform Edge Detection, Perform Dilation + Erosion, Close Gaps Between Edges
# ---------------------------------------------------------------------------- #
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

# ---------------------------------------------------------------------------- #
# Find Contours in the Edge Map
# ---------------------------------------------------------------------------- #
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

# ---------------------------------------------------------------------------- #
# Sort the Contours, Initialize Calibration Variable
# ---------------------------------------------------------------------------- #