from picamera2 import Picamera2
import cv2
import numpy as np

# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

print("Camera feed started. Press 'q' to quit.")

try:
    while True:
        # Capture frame as numpy array
        frame = picam2.capture_array()

        # Convert from RGB (picamera2 default) to BGR (OpenCV default)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Display the frame
        cv2.imshow("Camera Feed", frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    pass
finally:
    # Clean up
    picam2.stop()
    cv2.destroyAllWindows()
    print("Camera stopped.")