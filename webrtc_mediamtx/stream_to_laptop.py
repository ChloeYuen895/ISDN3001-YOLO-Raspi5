import subprocess
import signal
import sys
import time
import threading

def get_laptop_ip():
    """Replace with your laptop's IP address"""
    return "192.168.1.100"  # CHANGE THIS to your laptop's actual IP

def start_optimized_usb_stream():
    laptop_ip = get_laptop_ip()
    
    # Use MJPEG format for better performance with USB cameras
    cmd = [
        'ffmpeg',
        
        # USB Camera input settings - MJPEG format for better performance
        '-f', 'v4l2',
        '-input_format', 'mjpeg',      # Use MJPEG (more efficient for USB)
        '-framerate', '30',
        '-video_size', '640x480',      # Use 640x480 for lower latency
        '-i', '/dev/video0',           # Your working camera device
        
        # Video encoding settings
        '-c:v', 'libx264',             # Software H.264
        '-b:v', '1M',
        '-maxrate', '1M',
        '-bufsize', '2M',
        '-g', '30',                    # GOP size
        '-pix_fmt', 'yuv420p',
        
        # Ultra low latency settings
        '-tune', 'zerolatency',
        '-preset', 'ultrafast',
        '-fflags', 'nobuffer',
        '-flags', 'low_delay',
        
        # Stream to MediaMTX
        '-f', 'rtsp',
        '-rtsp_transport', 'tcp',      # More reliable
        f'rtsp://{laptop_ip}:8554/mystream'
    ]
    
    print("=" * 60)
    print("USB Camera Streaming Starting...")
    print(f"Camera: /dev/video0 (Integrated_Webcam_HD)")
    print(f"Streaming to: {laptop_ip}")
    print(f"Resolution: 640x480 @ 30fps")
    print(f"Format: MJPEG -> H.264")
    print("=" * 60)
    
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)
        
        # Monitor FFmpeg output in real-time
        def monitor_output():
            while process.poll() is None:
                output = process.stdout.readline()
                if output:
                    print(f"FFmpeg: {output.strip()}")
        
        monitor_thread = threading.Thread(target=monitor_output)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        return process
        
    except Exception as e:
        print(f"Error starting FFmpeg: {e}")
        return None

def signal_handler(sig, frame):
    print('\nStopping stream...')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    print("Raspberry Pi USB Camera Stream")
    print("Your camera supports: MJPEG & YUYV422 at 1280x720, 640x480")
    print("Press Ctrl+C to stop streaming")
    
    process = start_optimized_usb_stream()
    if process:
        # Wait for process to complete
        return_code = process.wait()
        print(f"FFmpeg process ended with return code: {return_code}")