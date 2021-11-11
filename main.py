## Created by Tapani Hopkins, 2021
## CC0 (i.e. free to use)



## Import and get arguments

# import standard modules
from os import listdir
from pathlib import Path

# import added modules
import configargparse

# import own modules
from analyse import Analyse

# get the options from "options.txt" or the command line (command line has priority)
p = configargparse.ArgParser(default_config_files=["options.txt"])
p.add("-b", "--min_brightness", type=int, default=10, help="how large a change in brightness [0-255?] is interpreted as movement")
p.add("-f", "--folderpath", type=str, help="folder where the video files are, can also give a path to a video file")
p.add("-s", "--min_size", type=float, default=325, help="how large an area (millionths of screen) has to move for it to be interpreted as a moving insect")
p.add("-S", "--max_size", type=float, default=40000, help="how small an area (millionths of screen) has to move for it to be interpreted as a moving insect")
p.add("-w", "--window", action="store_true", help="display what the computer sees in a window, good for debugging and for testing options")
options = p.parse_args()



## Initialise

# store the path as a Path object (easier to handle)
p = Path(options.folderpath)

# initialise the file counter
filecounter = 1

# list all the files in the given folder..
if (p.is_dir()):
    files = listdir(p)
   
# .. or just list the file if only one was given
#   (also store its parent folder)
else:
    files = [p.name]
    p = p.parent

# remove files that are not videos
for f in files:
    # mark any that are not mp4 or are hidden for removal
    remove = f.startswith(".") or not f.endswith(".mp4")
    
    # remove the non-videos from the list
    if (remove):
        files.remove(f)

# sort the file list
files.sort()



## Main loop

# analyse all the video files
for f in files:
    # get the absolute path of this video file
    path = str(p / f)
    
    # let the user know how far we've got
    print("")
    print("Video " + str(filecounter) + "/" + str(len(files)) + " : " + f)

    # count the number of moving insects in the video and save to file
    Analyse(path, min_brightness=options.min_brightness, min_size=options.min_size, max_size=options.max_size, window=options.window).start()
    
    # update the file counter
    filecounter += 1

