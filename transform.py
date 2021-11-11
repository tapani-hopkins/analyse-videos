## Created by Tapani Hopkins, 2021
## CC0 (i.e. free to use)

## Function for transforming video frames for motion detection.
## Called by 'analyse.py'.



# import
import cv2
import imutils

# function for transforming frames
def transform(frame):
    # resize the frame
    frame = imutils.resize(frame, width=300)
    
    # convert the frame to grayscale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # blur the frame
    frame = cv2.GaussianBlur(frame, (21, 21), 0)
    
    # return the frame
    return frame
