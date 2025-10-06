#!/usr/bin/env python3
import subprocess
import os

def test_camera_devices():
    """Test all available camera devices"""
    print("Testing USB Camera on Raspberry Pi...")
    print("Available video devices:")
    
    # List all video devices
    subprocess.run(['ls', '-la', '/dev/video*'])
    
    # Test each video device
    for i in range(5):
        device = f"/dev/video{i}"
        if os.path.exists(device):
            print(f"\n--- Testing {device} ---")
            
            # Test 1: List formats
            print("Supported formats:")
            cmd1 = ['ffmpeg', '-f', 'v4l2', '-list_formats', 'all', '-i', device]
            try:
                result1 = subprocess.run(cmd1, capture_output=True, text=True, timeout=10)
                print(result1.stderr if result1.stderr else "No format info available")
            except subprocess.TimeoutExpired:
                print("Timeout testing formats")
            
            # Test 2: Try to capture a test frame
            print(f"Testing frame capture on {device}...")
            cmd2 = [
                'ffmpeg',
                '-f', 'v4l2',
                '-i', device,
                '-t', '1',  # 1 second
                '-frames:v', '1',
                '-f', 'null',
                '-'
            ]
            try:
                result2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=15)
                if result2.returncode == 0:
                    print(f"✓ {device} is WORKING!")
                else:
                    print(f"✗ {device} has issues: {result2.stderr}")
            except subprocess.TimeoutExpired:
                print(f"✗ {device} timeout during capture test")

def quick_camera_check():
    """Quick check for working cameras"""
    print("Quick camera check...")
    cmd = ['v4l2-ctl', '--list-devices']
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout if result.stdout else "v4l2-ctl not available")
    
    # Alternative: use ffmpeg to list devices
    print("\nFFmpeg device list:")
    subprocess.run(['ffmpeg', '-f', 'v4l2', '-list_devices', 'true', '-i', '""'])

if __name__ == "__main__":
    print("USB Camera Diagnostic Tool")
    print("=" * 40)
    
    quick_camera_check()
    print("\n" + "=" * 40)
    test_camera_devices()