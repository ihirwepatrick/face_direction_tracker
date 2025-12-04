import cv2
import mediapipe as mp
import serial
import time

# Initialize MediaPipe Face Detection
mp_face = mp.solutions.face_detection
mp_draw = mp.solutions.drawing_utils
face_detection = mp_face.FaceDetection(min_detection_confidence=0.5)

# Connect to Arduino
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

# Camera setup
cap = cv2.VideoCapture(0)
CENTER_X = int(cap.get(3)) // 2
TOLERANCE = 30
STEP_DEGREE = 10

last_direction = "Center"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)

    if results.detections:
        detection = results.detections[0]
        bbox = detection.location_data.relative_bounding_box
        
        # Convert normalized coordinates to pixel coordinates
        h, w = frame.shape[:2]
        x = int(bbox.xmin * w)
        y = int(bbox.ymin * h)
        width = int(bbox.width * w)
        height = int(bbox.height * h)
        
        cx = x + width // 2
        cy = y + height // 2

        # Draw face box and center point
        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

        # Calculate offset and control motor
        offset = cx - CENTER_X
        
        if offset > TOLERANCE and last_direction != "Right":
            arduino.write(f'CW {STEP_DEGREE}\n'.encode())
            last_direction = "Right"
        elif offset < -TOLERANCE and last_direction != "Left":
            arduino.write(f'CCW {STEP_DEGREE}\n'.encode())
            last_direction = "Left"
        elif abs(offset) <= TOLERANCE:
            last_direction = "Center"

        cv2.putText(frame, f"{last_direction} | {offset}px", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "No face detected", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        last_direction = "Center"

    cv2.imshow("Face Tracker", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()

