## Created by Tapani Hopkins, 2021
## CC0 (i.e. free to use)

## Get metadata on a video file,
## such as its fps, length, dimensions,
## and whether it is a valid video file or not.
## If passed a transform, gives the dimensions of a transformed frame.
## Called by 'analyse.py'.



# import
import cv2
from pathlib import Path
from time import sleep

class VideoData:
    def __init__(self, filepath, transform=None):
        # convert the path to a Path object (easier to handle)
        p = Path(filepath)
        
        # get the path in the local format
        # (may help Windows paths run on Mac and vice versa),
        # and the file/folder name
        self.path = str(p)
        self.name = p.parts[-1]
        
        # open the file to get the video properties
        v = cv2.VideoCapture(self.path)
        sleep(0.1)
        
        # get the video fps and number of frames
        self.fps = v.get(cv2.CAP_PROP_FPS)
        self.frames = v.get(cv2.CAP_PROP_FRAME_COUNT)
        
        # check that the file exists and is a mp4
        self.valid = p.exists() and (p.suffix == ".mp4")
        
        # check that the file contains valid video
        if (self.fps==0 or self.frames==0):
            self.valid = False
        
        # if the video is valid, get its dimensions and length..
        if (self.valid):
            # get the first frame
            frame = v.read()[1]
            
            # transform the first frame
            if (transform):
                frame = transform(frame)
        
            # get the video dimensions (of the transformed frame)
            self.width = frame.shape[1]
            self.height = frame.shape[0]
            
            # get the length in seconds
            self.length = self.frames / self.fps
        
        # .. if the video is not valid, set its dimensions and length to 0
        else:
            self.width = 0
            self.height = 0
            self.length = 0
        
        # close the file
        v.release()
