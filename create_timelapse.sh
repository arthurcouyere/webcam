#!/bin/bash

inputFolder=capture
outputFile=timelapse.mp4

cd $(dirname $0)

if [ -f $outputFile ]; then rm -f $outputFile; fi	
ffmpeg -loglevel info -r 24 -pattern_type glob -i "$inputFolder/*.jpg" -s hd1080 -vcodec libx264 $outputFile
