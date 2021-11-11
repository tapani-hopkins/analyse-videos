## Created by Tapani Hopkins, 2021
## Partly based on code by Adrian Rosebrock:
## https://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/
## CC0 (i.e. free to use) as far as Tapani is concerned.
## Adrian Rosebrock's code is free to use EXCEPT if you are developing a course, book, or other educational product. See his license for details, in "PyImageSearch license.txt".

## Detect movement in images or frames of video
## Compares each new frame with the average of the previous frames
## Checks if the brightness of individual pixels has changed significantly,
## and such changed pixels form a roughly insect-sized area
## Returns the number of insect-sized areas that have moved, and (optionally) their bounding boxes.
## Called by 'analyse.py'



# import
import cv2
from copy import copy
import imutils

class MotionCounter:
    def __init__(self, min_brightness_change, min_size, max_size, boxes=False):
        # store the minimum brightness change (0–255?),
        # minimum size and maximum size (pixels^2)
        # that will be interpreted as movement
        self.min_brightness_change = min_brightness_change
        self.min_size = min_size
        self.max_size = max_size
        
        # store whether to return bounding box coordinates or not
        self.boxes = boxes
        
        # initialise the averaged out frame (average of past frames)
        self.avg = None
        
    def check(self, frame):
        # initialise the number of moving objects
        n = 0
        
        # initialise the bounding boxes of moving objects, if asked for..
        if (self.boxes):
            boxes = []
            
        # ..if not asked for the boxes, return "None"
        else:
            boxes = None
        
        # if the average frame is None, initialise it and stop processing the frame
        if self.avg is None:
            self.avg = frame.copy().astype("float")
            if (self.boxes):
                return (0, boxes)
                
            else:
                return (0, None)
    
        # accumulate the weighted average between the current frame and
        # previous frames, then compute the difference between the current
        # frame and the running average
        cv2.accumulateWeighted(frame, self.avg, 0.5)
        frameDelta = cv2.absdiff(frame, cv2.convertScaleAbs(self.avg))
        
        # check which pixels have significantly changed in brightness
        thresh = cv2.threshold(frameDelta, self.min_brightness_change, 255, cv2.THRESH_BINARY)[1]
        
        # dilate the thresholded image to fill in holes
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # find contours on the thresholded image
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        
        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < self.min_size:
                continue
        
            # if the contour is too big (i.e. likely a shadow), ignore it
            if cv2.contourArea(c) > self.max_size:
                continue
            
            # count this contour
            n = n+1
            
            # compute the bounding box for the contour if asked to do so
            if (self.boxes):
                (x, y, w, h) = cv2.boundingRect(c)
                boxes.append( (x, y, w, h) )
        
        # return the number of moving objects, and their bounding boxes
        return (n, boxes)
