#webcam

Simple webcam kit to take pictures at fixed interval in order to make a timelaspse

3 tools :
- webcam.sh : script that takes pictures
- chek_light.py : script that checks if it's night or day (in my case, webcam.sh call check_light.py and does not take any picture during night, since I use a simple raspicam with no light or flash)
- dropbox_upload.py : script that uploads the pictures to your dropbox account
