# Import necessary libraries
import cv2
import mediapipe as mp
import pyautogui

# Initialize the camera
cam = cv2.VideoCapture(0)

# Initialize Face Mesh from Mediapipe
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

# Get the screen size for mouse control
screen_w, screen_h = pyautogui.size()

# Main loop for capturing and processing video frames
while True:
    # Read a frame from the camera
    _, frame = cam.read()

    # Flip the frame horizontally for better user experience
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB format for Mediapipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame using Face Mesh
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape

    # Check if facial landmarks are detected
    if landmark_points:
        landmarks = landmark_points[0].landmark

        # Draw circles on specific facial landmarks for visualization
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))

            # Move the mouse cursor to the specified landmark
            if id == 1:
                screen_x = screen_w * landmark.x
                screen_y = screen_h * landmark.y
                pyautogui.moveTo(screen_x, screen_y)

        # Extract left eye landmarks for additional visualization
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 300, 300))

        # Check if the difference in y-coordinates of left eye landmarks is less than a threshold for right-click
        if (left[0].y - left[1].y) < 0.004:
            # Implement the right-click action
            pyautogui.rightClick()
            # Add a delay to avoid multiple right-clicks in rapid succession
            pyautogui.sleep(1)

    # Display the frame with annotations
    cv2.imshow('Eye Controlled Mouse', frame)

    # Wait for a key press event to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cam.release()
cv2.destroyAllWindows()
