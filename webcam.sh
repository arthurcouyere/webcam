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
