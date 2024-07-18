# Eye Controlled Mouse

This project uses OpenCV, Mediapipe, and PyAutoGUI to control the mouse cursor with eye movements. It leverages facial landmark detection to track eye movements and translate them into mouse actions.

## Prerequisites

- Python 3.x
- OpenCV
- Mediapipe
- PyAutoGUI

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/eye-controlled-mouse.git
    cd eye-controlled-mouse
    ```

2. Install the required libraries:

    ```sh
    pip install opencv-python mediapipe pyautogui
    ```

## Usage

1. Run the script:

    ```sh
    python eye_controlled_mouse.py
    ```

2. The script will initialize your webcam and start detecting your facial landmarks. The mouse cursor will move based on the specified facial landmarks.

3. To right-click, close your left eye. The script detects this by checking if the difference in y-coordinates of specific left eye landmarks is less than a threshold.

4. Press `q` to exit the program.

## Code Explanation

### Import necessary libraries

```python
import cv2
import mediapipe as mp
import pyautogui
```

### Initialize the camera and Face Mesh from Mediapipe

```python
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
```

### Get the screen size for mouse control

```python
screen_w, screen_h = pyautogui.size()
```

### Main loop for capturing and processing video frames

```python
while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            if id == 1:
                screen_x = screen_w * landmark.x
                screen_y = screen_h * landmark.y
                pyautogui.moveTo(screen_x, screen_y)

        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 300, 300))

        if (left[0].y - left[1].y) < 0.004:
            pyautogui.rightClick()
            pyautogui.sleep(1)

    cv2.imshow('Eye Controlled Mouse', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
```

### Explanation

- The script captures video frames from the webcam and flips them horizontally for a better user experience.
- The frames are converted to RGB format and processed using Mediapipe's Face Mesh to detect facial landmarks.
- Specific facial landmarks are tracked to control the mouse cursor.
- If the difference in y-coordinates of specific left eye landmarks is less than a threshold, a right-click action is triggered.
- The script displays the frame with annotations and waits for a key press event to exit the loop.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

---
