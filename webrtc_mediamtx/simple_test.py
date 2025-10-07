#!/usr/bin/env python3
import subprocess
import time

def test_camera_direct():
    """Test camera with simple FFmpeg command"""
    print("Testing camera with simple FFmpeg command...")
    
    cmd = [
        'ffmpeg',
        '-f', 'v4l2',
        '-input_format', 'mjpeg',
        '-video_size', '640x480',
        '-i', '/dev/video0',
        '-t', '10',  # Run for 10 seconds
        '-f', 'null',
        '-'
    ]
    
    try:
        print("Starting camera test (10 seconds)...")
        process = subprocess.Popen(cmd, stderr=subprocess.PIPE, universal_newlines=True)
        
        # Read output in real-time
        for line in process.stderr:
            if 'frame=' in line:
                print(f"Progress: {line.strip()}")
        
        process.wait()
        print("Camera test completed successfully!")
        
    except Exception as e:
        print(f"Camera test failed: {e}")

if __name__ == "__main__":
    test_camera_direct()