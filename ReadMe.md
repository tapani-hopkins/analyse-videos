 
 # Analyse insect camera videos
 
 Python script for going through videos from an insect camera, and counting how many insects moved in each frame.
 
 Saves the results (number of moving insects in each frame) to file. Also saves info on each video (e.g. fps) to a separate file. 
 
 Currently very approximate. Gives a very rough indication of how many insects are active.
 
 The main file is 'main.py'. It lists all the video files and passes them one at a time to 'analyse.py', which analyses them using the other files. (Some day, I'll work out how to package python scripts)
 
- main.py
    - analyse.py
        - filevideostream.py
        - motioncounter.py
        - transform.py
        - videodata.py
        
## Required packages

You must have the following python packages installed:

- ConfigArgParse
- imutils
- opencv-contrib-python

I generally create a virtual environment into which I install them (that way, they can be easily uninstalled by deleting the folder). For example, in Mac Terminal:

    # go to desired folder (make sure there are no spaces in the folder path)
    cd /Users/tapani/T/Courses/2020_insect_camera/analyse_videos
    
    # create virtual environment 'env'
    python3 -m venv env
    
    # open the environment
    source env/bin/activate
    
    # install python modules to 'env'
    pip3 install ConfigArgParse
    pip3 install imutils
    pip3 install opencv-contrib-python==4.1.0.25

## Running

1. Go to the folder.

    `cd /Users/tapani/T/Courses/2020_insect_camera/analyse_videos`

2. If you downloaded the required packages to a virtual environment, open it.
    
    `source env/bin/activate`

3. Write the path to the folder which contains the videos in 'options.txt'.

    folderpath = "/Users/tapani/T/Courses/2020_insect_camera/Temporary copies of videos"
    
4. Run the script.

    `python3 main.py`

The script will analyse all the videos in the folder, and save the results in two csv files. 

Currently, only mp4 videos are checked, anything else is ignored.

### Options

The following options can be changed in options.txt.

- **folderpath**
    - Path to the folder in which the videos are. Can also be set to a single video file.
- **window**
    - If `True`, the computer shows what it is doing in a window, and puts boxes around what it believes to be moving insects. Very useful for figuring out the correct settings for motion detection.
- **min_brightness**
    - How large a brightness change is to be interpreted as movement. Larger values = brightness of a pixel has to change considerably for the computer to interpret it as movement. Increase this value if mild changes in lighting, shadows etc are showing up as movement.
- **min_size**
    - How large a moving object has to be. (minimum size in millionths of screen area) Increase this if tiny, random changes in just a few pixels are showing up as movement.
- **max_size**
    - How small a moving object has to be. (maximum size in millionths of screen area) Decrease this if sudden shadows, the sun going behind a cloud etc are showing up as movement.

### Results

The results are stored in two csv files, which by default are called:

- insects_per_frame.csv
    - Each frame on a separate row. Columns: video name, frame number, number of moving insects.
- video_info.csv
    - Each video file on a separate row. Columns: video name, valid readable video (True/False), FPS, number of frames, length in seconds.

## License

As far as I am concerned, this is CC0, i.e. 

> Feel free to use any way you want!

**However**, some of the files are partly based on code by [Adrian Rosebrock](https://github.com/jrosebr1). See the licenses (in folder 'licenses') for more info. These files are clearly marked at the start of the file.

If you use this code at length or in a more formal context, do consider citing it. It makes it easier for others to find it, and I get to know that the code is useful.
