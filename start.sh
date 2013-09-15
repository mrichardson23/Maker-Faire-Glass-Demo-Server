#!/bin/bash
mjpg_streamer -i "/usr/lib/input_uvc.so -d /dev/video0 -r 320x180 -f 5" -o "/usr/lib/output_http.so -p 8090 -w /var/www" &
python listener.py
