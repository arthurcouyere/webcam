#!/bin/bash

curDir=$(dirname $0)
curDate=$(date +"%Y-%m-%d_%H%M")
outputDir=$curDir/capture
outputFile=$outputDir/$curDate.jpg

mkdir -p $outputDir

# check sunrise and sunset
$curDir/virtualenv/bin/python $curDir/check_light.py
if [ $? -ne 0 ]; then exit 1; fi

# raspi camera
raspistill -o $outputFile

# webcam
#fswebcam -r 640x480 --no-banner $outputFile

# ip webcam
#cd $outputDir
#wget --no-proxy http://192.168.1.24:8080/photo.jpg
#mv photo.jpg $outputFile
