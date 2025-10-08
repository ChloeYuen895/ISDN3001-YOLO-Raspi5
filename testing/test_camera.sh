lsusb  # Lists USB devices; note your camera
v4l2-ctl --list-devices  # Should show /dev/video0 (or /dev/video1)
v4l2-ctl -d /dev/video0 --list-formats-ext  # Check supported resolutions/FPS (e.g., 1280x720@30fps)

ffmpeg -f v4l2 -input_format mjpeg -framerate 30 -video_size 640x480 -i /dev/video0 -c:v libx264 -preset ultrafast -b:v 800k -t 5 test_lowres.mp4