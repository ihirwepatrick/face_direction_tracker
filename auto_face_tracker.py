import cv2
import time
import serial

# Connect to Arduino (adjust COM port)
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start webcam
cap = cv2.VideoCapture(0)
frame_width = int(cap.get(3))
CENTER_X = frame_width // 2
TOLERANCE = 30  # pixels from center before motor moves
STEP_DEGREE = 10  # motor rotation step in degrees

# Track last movement to avoid continuous commands
last_direction = "Center"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        x, y, w, h = faces[0]
        cx = x + w // 2
        cy = y + h // 2

        # Draw visuals
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

        offset = cx - CENTER_X

        # Decide if motor should move
        if offset > TOLERANCE and last_direction != "Right":
            arduino.write(f'CW {STEP_DEGREE}\n'.encode())
            last_direction = "Right"
        elif offset < -TOLERANCE and last_direction != "Left":
            arduino.write(f'CCW {STEP_DEGREE}\n'.encode())
            last_direction = "Left"
        elif abs(offset) <= TOLERANCE:
            last_direction = "Center"  # stop motor commands

        # Display text
        direction_text = f"Direction: {last_direction} | Offset: {offset}px"
        cv2.putText(frame, direction_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 255, 0), 2)

    else:
        cv2.putText(frame, "Face not detected", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        last_direction = "Center"

    cv2.imshow("Accurate Face Tracker Motor", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()