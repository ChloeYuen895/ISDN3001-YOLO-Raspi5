#!/bin/bash

SERVER_IP="100.80.197.71" # Replace with your server's IP address
STREAM_URL="rtsp://$SERVER_IP:8554/cam1"

echo "Starting camera stream to $STREAM_URL"
echo "Stream is active - check your laptop at http://localhost:5000/"

# Clean version with suppressed warnings
ffmpeg -f v4l2 \
       -input_format mjpeg \
       -video_size 640x480 \
       -framerate 30 \
       -i /dev/video0 \
       -c:v libx264 \
       -preset ultrafast \
       -tune zerolatency \
       -f rtsp \
       -rtsp_transport tcp \
       -loglevel error \
       "$STREAM_URL"