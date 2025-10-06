#!/bin/bash
echo "Testing USB Camera Stream..."
echo "Camera: /dev/video0"

# Test raw camera feed
echo "1. Testing raw camera feed..."
ffmpeg -f v4l2 -input_format mjpeg -video_size 640x480 -i /dev/video0 -t 5 -f null - > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✓ Camera feed test PASSED"
else
    echo "✗ Camera feed test FAILED"
    exit 1
fi

# Test encoding
echo "2. Testing H.264 encoding..."
ffmpeg -f v4l2 -input_format mjpeg -video_size 640x480 -i /dev/video0 -t 3 -c:v libx264 -preset ultrafast -tune zerolatency -f null - > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✓ Encoding test PASSED"
else
    echo "✗ Encoding test FAILED"
    exit 1
fi

echo "All tests passed! Camera is ready for streaming."