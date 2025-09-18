from picamera2 import Picamera2

# List available cameras
print("Available cameras:", Picamera2.global_camera_info())

# Initialize camera
picam2 = Picamera2()
print("Camera initialized successfully")
picam2.start()
print("Camera started")
picam2.stop()