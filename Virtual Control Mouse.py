import cv2
import mediapipe as mp
import pyautogui
import math

# Disable PyAutoGUI fail-safe
pyautogui.FAILSAFE = False

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_x, index_y = 0, 0
middle_finger_clicked = False

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=20, color=(100, 255, 255))
                    index_x = int(screen_width / frame_width * x)
                    index_y = int(screen_height / frame_height * y)

                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=20, color=(100, 255, 255))
                    thumb_x = int(screen_width / frame_width * x)
                    thumb_y = int(screen_height / frame_height * y)

                    # Move the mouse cursor
                    pyautogui.moveTo(index_x, index_y)

                    # Perform a click if fingers are close
                    if abs(index_y - thumb_y) < 20:
                        pyautogui.mouseDown()
                        pyautogui.sleep(1)  # Adjust the duration as needed
                        pyautogui.mouseUp()

                    # Scroll up or down based on the distance between thumb and index finger
                    distance = math.sqrt((thumb_x - index_x)**2 + (thumb_y - index_y)**2)
                    if distance > 100:
                        pyautogui.scroll(1)  # Scroll up
                    elif distance < 50:
                        pyautogui.scroll(-1)  # Scroll down

                if id == 12:  # Assuming middle finger
                    if landmarks[8].y < landmarks[12].y:  # Check if middle finger is below index finger
                        middle_finger_clicked = True
                    else:
                        middle_finger_clicked = False

                    # Perform right-click if middle finger is below index finger
                    if middle_finger_clicked:
                        pyautogui.rightClick()

    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)
