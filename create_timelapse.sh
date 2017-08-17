#!/bin/bah

inputFolder=capture
outputFile=timelapse.mp4

ffmpeg -r 24 -pattern_type glob -i '$inputFolder/*.jpg' -s hd1080 -vcodec libx264 $outputFile
