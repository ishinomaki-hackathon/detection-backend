import cv2
import mediapipe as mp

# Initialize MediaPipe Pose model for body detection
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Open a video capture stream (you can replace this with a camera feed)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Pose model
    results = pose.process(frame_rgb)

    if results.pose_landmarks is not None:
        # Count the number of detected bodies
        num_bodies = len(results.pose_landmarks.landmark) // 33  # Each body has 33 landmarks

        for i in range(num_bodies):
            # Extract landmark coordinates for each detected body
            body_landmark_list = [(landmark.x, landmark.y) for landmark in results.pose_landmarks.landmark[i * 33:(i + 1) * 33]]
            h, w, _ = frame.shape

            # Draw circles on body landmarks for each detected body
            for x, y in body_landmark_list:
                x_pixel, y_pixel = int(x * w), int(y * h)
                cv2.circle(frame, (x_pixel, y_pixel), 7, (0, 0, 255), -1)  # Larger red circles

            # Define connections between landmarks to form the body skeleton
            connections = [
                (11, 12), (12, 24), (11, 23),  # Left Arm
                (23, 24), (24, 26), (26, 28),  # Left Leg
                (12, 14), (14, 16),           # Neck and Spine
                (11, 13), (13, 15),           # Right Arm
                (23, 25), (25, 27)            # Right Leg
            ]

            # Draw lines connecting body landmarks to form the skeleton for each detected body
            for connection in connections:
                start_x, start_y = body_landmark_list[connection[0] - (i * 33)]
                end_x, end_y = body_landmark_list[connection[1] - (i * 33)]
                start_x_pixel, start_y_pixel = int(start_x * w), int(start_y * h)
                end_x_pixel, end_y_pixel = int(end_x * w), int(end_y * h)
                cv2.line(frame, (start_x_pixel, start_y_pixel), (end_x_pixel, end_y_pixel), (0, 255, 0), 2)

    # Display the frame with body and hand landmarks
    cv2.imshow("Body and Hand Landmarks", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
