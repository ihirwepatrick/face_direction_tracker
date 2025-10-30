import cv2
import time

# Load the face detector (Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start the webcam
cap = cv2.VideoCapture(0)

prev_cx, prev_cy = 0, 0
prev_time = time.time()
direction = "Center"
speed = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale (for better face detection)
    # uses one color channle (light instensity for better and more reliable results instad of RGB)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Process the first detected face (keep it simple)
    for (x, y, w, h) in faces:
        # Draw a green box around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Find the center of the face
        cx = x + w // 2
        cy = y + h // 2

        # Draw the center point
        cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

        # Calculate movement and time difference
        curr_time = time.time()
        dt = curr_time - prev_time if prev_time else 0.1
        dx = cx - prev_cx
        dy = cy - prev_cy

        # Compute speed in pixels per second
        dist = (dx**2 + dy**2) ** 0.5
        speed = dist / dt if dt > 0 else 0

        # Determine direction
        if abs(dx) > abs(dy):
            if dx > 10:
                direction = "Right"
            elif dx < -10:
                direction = "Left"
        else:
            if dy > 10:
                direction = "Down"
            elif dy < -10:
                direction = "Up"

        # Update previous values
        prev_cx, prev_cy = cx, cy
        prev_time = curr_time

        # Display direction and speed
        text = f"Direction: {direction} | Speed: {int(speed)} px/s"
        print(text)
        cv2.putText(frame, text, (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        break  # Only track one face [Only one face is being trakced here]

    # Show the live frame
    cv2.imshow('Face Direction Tracker', frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


#you have to make sure that the camer has got enough ligthing for the face to be detected