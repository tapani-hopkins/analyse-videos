## Created by Tapani Hopkins, 2021
## Partly based on code by Adrian Rosebrock:
## https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/
## CC0 (i.e. free to use) as far as Tapani is concerned.
## Adrian Rosebrock's code is free to use EXCEPT if you are developing a course, book, or other educational product. See his license for details, in "PyImageSearch license.txt".

## Detect movement in the frames of a video,
## and save the number of moving insects in each frame in a file.
## Called by 'main.py'



## Import and get arguments

# import standard modules
import time

# import added modules
import configargparse
import cv2

# import own modules
from filevideostream import FileVideoStream
from motioncounter import MotionCounter
from transform import transform
from videodata import VideoData

class Analyse:
    def __init__(self, filepath, resultfile="insects_per_frame.csv", videoinfofile="video_info.csv" , min_brightness=5, min_size=300, max_size=10000, window=False):
        # store whether to show what the computer sees in a window
        self.window = window

        # get the fps, dimensions, name etc of the transformed video
        self.video = VideoData(filepath, transform=transform)
        
        # save info on the video to file
        # (file name, if it is a valid video, fps, number of frames, length in seconds)
        f = open(videoinfofile, "a", encoding="utf-8")
        f.write(self.video.name + u"," + str(self.video.valid) + u"," + str(self.video.fps) + u"," + str(self.video.frames) + u"," + str(self.video.length) + u"\n")
        f.close()
        
        # if this is not a valid video file, stop processing it
        if (not self.video.valid):
            print("Ignoring file " + self.video.name + ", does not contain valid video.")
            return
        
        # convert the min and max sizes from millionths of screen area to pixels^2
        A = self.video.width * self.video.height
        min_size2 = int(min_size * 1e-6 * A)
        max_size2 = int(max_size * 1e-6 * A)

        # initialise a motion detector which checks frames for moving insects
        self.motion = MotionCounter(min_brightness, min_size2, max_size2, boxes=self.window)

        # initialise the frame counter
        self.frameCount = 0
        
        # initialise a boolean saying if it is time to stop the analysis
        self.stopped = False

        # start reading frames in a separate thread
        # frames (up to 128 at a time) are transformed and stored in 'fsv'
        # only read one frame a second, ignore rest
        self.fvs = FileVideoStream(self.video.path, transform=transform, skip=self.video.fps).start()
        time.sleep(0.1)

        # open the file in which the results will be saved
        self.f = open(resultfile, "a", encoding="utf-8")

    def start(self):
        # do nothing if the video is not valid
        if (not self.video.valid):
            return
    
        # keep looping until all frames have been processed
        while self.fvs.running() and not self.stopped:
            # get the next frame
            frame = self.fvs.read()
            
            # update the frame counter
            self.frameCount += 1
    
            n, boxes = self.motion.check(frame)
            
            # write the number of moving insects in this frame to file
            self.f.write(self.video.name + u"," + str(self.frameCount) + u"," + str(n) + u"\n")
    
            # if displaying the window, draw boxes around moving insects and log keyboard input
            if self.window:
                # draw the bounding boxes on the frame
                for x, y, w, h in boxes:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
    
                # show the frame
                cv2.imshow("Frame", frame)
        
                # stop the loop if the user presses 'q'
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
              
        # when all the frames have been processed, stop
        if (not self.stopped):
            self.stop()

    def stop(self):
        # tell the loop (in start()) to stop
        self.stopped = True
    
        # close the file in which results are saved
        self.f.close()

        # close any windows (may not work on Mac)
        cv2.destroyAllWindows()

        # stop reading frames
        if not self.fvs.stopped:
            self.fvs.stop()
            
