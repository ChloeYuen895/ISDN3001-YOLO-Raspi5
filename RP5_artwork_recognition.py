import cv2
import numpy as np
from picamera2 import Picamera2
from ultralytics import YOLO

# Load the YOLO model
model = YOLO("/home/ytyuenab/RP5/models/best_studio_v2.onnx", task = "segment")
# /home/ytyuenab/RP5/models/best_studio_detect.onnx
# /home/ytyuenab/RP5/models/best_studio_v2.onnx, task = "segment"

# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

# Set image size and confidence threshold
imgsz = 640
conf = 0.75

print("Camera feed started. Press 'q' to quit.")

try:
    while True:
        # Capture frame as numpy array
        frame = picam2.capture_array()

        # Convert from RGB (picamera2 default) to BGR (OpenCV default)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Perform segmentation on CPU
        results = model.predict(source=frame, imgsz=imgsz, conf=conf, device="cpu")

        # Process results
        annotated_frame = results[0].plot()  # Plot segmentation masks and labels

        # Display the frame with segmentation
        cv2.imshow("Artwork Recognition", annotated_frame)

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