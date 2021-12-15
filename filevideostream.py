## From the imutils package
## https://github.com/PyImageSearch/imutils/blob/c12f15391fcc945d0d644b85194b8c044a392e0a/imutils/video/filevideostream.py
## Minor modifications by Tapani Hopkins
## This is basically the same as in the package, except for two changes:
## - bug fix ('break' in line 80)
## - option to only process e.g. every third frame ('skip')

## Reads frames from a video, transforms them, and stores them for other threads to use.
## Faster to do this in a separate thread, so the other scripts don't need to wait for each frame to decode.



# import
from threading import Thread
import cv2
import sys
import time

# import the Queue class from Python 3
if sys.version_info >= (3, 0):
    from queue import Queue

# otherwise, import the Queue class for Python 2.7
else:
    from Queue import Queue


class FileVideoStream:
    def __init__(self, path, transform=None, skip=None, queue_size=128):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.stream = cv2.VideoCapture(path)
        self.stopped = False
        
        # store the transforms to be done on each frame
        self.transform = transform
        
        # add every frame to the queue..
        if (skip is None):
            self.skip = 1
            
        # .. or if asked to do so, store how often frames are to be added to the queue
        else:
            self.skip = skip

        # initialise the queue in which the decoded and transformed frames will be stored
        self.Q = Queue(maxsize=queue_size)
        
        # initalise the thread
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True

        # initialise the frame counter (used to pick every skip:th frame)
        self.frameCounter = 0

    def start(self):
        # start a thread to read frames from the file video stream
        self.thread.start()
        return self

    def update(self):
        # keep looping infinitely
        while True:
            # if asked to stop, stop the thread..
            if self.stopped:
                break

            # ..otherwise, add a frame if there is space in the queue
            if not self.Q.full():
                # read the next frame from the file
                (grabbed, frame) = self.stream.read()

                # update the frame counter
                self.frameCounter += 1
                
                # if the `grabbed` boolean is `False`, we have
                # reached the end of the video file
                if not grabbed:
                    self.stopped = True
                    break
                    
                # only store every 'skip'th frame
                if (self.frameCounter % self.skip == 0):
                    # if there are transforms to be done,
                    # transform the frame before storing in the queue
                    if self.transform:
                        frame = self.transform(frame)

                    # add the frame to the queue
                    self.Q.put(frame)
               
            # if the queue is full, wait a while
            else:
                time.sleep(0.1)
        
        # release the video stream when finished
        self.stream.release()

    def read(self):
        # return next frame in the queue
        return self.Q.get()

    def running(self):
        # return True if there are still frames on the way (either in the queue or coming from the stream)
        return self.more() or not self.stopped

    def more(self):
        # return True if there are still frames in the queue. If stream is not stopped, try to wait a moment
        tries = 0
        while self.Q.qsize() == 0 and not self.stopped and tries < 5:
            time.sleep(0.1)
            tries += 1

        return self.Q.qsize() > 0

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        
        # wait until stream resources are released (producer thread might be still grabbing frame)
        self.thread.join()
