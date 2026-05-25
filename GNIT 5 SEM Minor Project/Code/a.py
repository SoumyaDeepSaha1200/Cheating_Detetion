import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import time

# Load images from the 'student_images' folder
path = 'student_images'
images = []
classNames = []
mylist = os.listdir(path)
for cl in mylist:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

# Initialize variables
attendance_records = {}  # Dictionary to hold attendance records with last marked time
write_interval = 10  # Interval in seconds to write to CSV
last_written_time = time.time()  # Track the last written time
warnings = {}  # Dictionary to track warnings for each student
warning_threshold = 10  # Threshold for warnings before cancelling exam
frame_count_to_warn = 30  # Number of consecutive frames to detect face disappearance
face_disappearance_warnings = {}  # Dictionary to track face disappearance warnings
person_detected = {}  # Dictionary to track if person is detected
person_movement_warnings = {}  # Dictionary to track person movement warnings
movement_warning_threshold = 30  # Threshold for movement warnings before cancelling exam

# Encode faces from the loaded images
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encoded_face = face_recognition.face_encodings(img)[0]
            encodeList.append(encoded_face)
        except IndexError:
            print("No face found in the image")
    return encodeList

encoded_face_train = findEncodings(images)

def write_attendance_to_csv(attendance_records):
    file_path = 'output.csv'
    with open(file_path, 'a') as f:
        # Check if the file is empty, and if so, write headers
        if f.tell() == 0:
            f.write("Name,Head Movement,Left Eye,Right Eye,Head Position,Date,Time,Cheating Incident\n")
        # Write all records
        for record in attendance_records.values():
            f.write(f"{record['Name']},{record['Head Movement']},{record['Left Eye']},{record['Right Eye']},{record['Head Position']},{record['Date']},{record['Time']},{record['Cheating Incident']}\n")

def markAttendance(name, head_movement_angle, left_eye_state, right_eye_state, head_position, cheating_incident=None):
    now = datetime.now()
    date = now.strftime('%d-%B-%Y')
    time_str = now.strftime('%I:%M:%S:%p')
    if name not in attendance_records or (time.time() - attendance_records[name]["Last Marked"]) >= 10:
        attendance_records[name] = {
            "Name": name,
            "Head Movement": f"{head_movement_angle:.2f} degrees" if name != "No person" else head_movement_angle,
            "Left Eye": left_eye_state,
            "Right Eye": right_eye_state,
            "Head Position": head_position,
            "Date": date,
            "Time": time_str,
            "Cheating Incident": cheating_incident,
            "Last Marked": time.time()
        }
        warnings[name] = 0  # Reset warnings for the student if marked
    else:
        warnings[name] += 1  # Increment warnings for the student
        if warnings[name] >= warning_threshold:
            print(f"WARNING: {name} has exceeded warning threshold. Cancelling exam for cheating.")
            # Clear attendance record and warnings for the student
            del attendance_records[name]
            del warnings[name]

def angle_between_points(p1, p2):
    # Calculate angle in radians
    angle_radians = np.arctan2(p2[1] - p1[1], p2[0] - p1[0])
    # Convert to degrees
    angle_degrees = np.degrees(angle_radians)
    return angle_degrees

def calculate_head_movement_angle(landmarks):
    # Extract relevant landmarks for head movement calculation
    left_eye_center = np.mean(landmarks['left_eye'], axis=0)
    right_eye_center = np.mean(landmarks['right_eye'], axis=0)

    # Calculate the head movement angle
    head_movement_angle = angle_between_points(left_eye_center, right_eye_center)

    return head_movement_angle

def eye_aspect_ratio(eye):
    # Calculate the Euclidean distances between the vertical eye landmarks
    vertical_dist1 = np.linalg.norm(np.array(eye[1]) - np.array(eye[5]))
    vertical_dist2 = np.linalg.norm(np.array(eye[2]) - np.array(eye[4]))

    # Calculate the Euclidean distance between the horizontal eye landmarks
    horizontal_dist = np.linalg.norm(np.array(eye[0]) - np.array(eye[3]))

    # Calculate the eye aspect ratio
    ear = (vertical_dist1 + vertical_dist2) / (2.0 * horizontal_dist)

    return ear

def determine_head_position(landmarks):
    nose_point = landmarks['nose_bridge'][3]  # Taking a point on the nose bridge for reference
    chin_point = landmarks['chin'][8]  # Taking a point on the chin for reference

    # Check if the denominator is zero
    if chin_point[0] == nose_point[0]:
        return "Not Moving"

    # Calculate the slope of the line connecting the nose and chin points
    slope = (chin_point[1] - nose_point[1]) / (chin_point[0] - nose_point[0])

    # Calculate the angle of this slope with respect to the horizontal
    angle = np.degrees(np.arctan(slope))

    # Determine the head position based on the angle
    if angle > 10:
        return "Tilted Down"
    elif angle < -10:
        return "Tilted Up"
    elif angle > 5:
        return "Tilted Right"
    elif angle < -5:
        return "Tilted Left"
    else:
        return "Not Moving"

# Open the webcam
cap = cv2.VideoCapture(0)

# Cheating threshold
cheating_threshold = 30  # Adjust as needed

# Continuous talking check
talk_start_time = None
talk_duration_threshold = 180  # 3 minutes

while True:
    success, img = cap.read()

    if not success:
        print("Failed to capture an image from the webcam.")
        break

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)

    if imgS.size == 0:
        print("Resized image is empty. Skipping this frame.")
        continue

    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    faces_in_frame = face_recognition.face_locations(imgS)
    encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)

    if not faces_in_frame:
        # No faces detected, assume no person in the screen
        print("No person in the screen.")
        for name in person_detected.keys():
            person_detected[name] = False
        markAttendance("No person", 0, "N/A", "N/A", "N/A")

    else:
        for encode_face, faceloc in zip(encoded_faces, faces_in_frame):
            name = "Unknown"
            matches = face_recognition.compare_faces(encoded_face_train, encode_face)
            faceDist = face_recognition.face_distance(encoded_face_train, encode_face)
            matchIndex = np.argmin(faceDist)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper().lower()
                y1, x2, y2, x1 = faceloc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Calculate head movement angle using face landmarks
                landmarks = face_recognition.face_landmarks(imgS, [faceloc])[0]
                head_movement_angle = calculate_head_movement_angle(landmarks)

                # Inside the main loop, after obtaining landmarks
                head_position = determine_head_position(landmarks)

                # Calculate eye aspect ratio for left and right eyes
                left_eye = landmarks['left_eye']
                right_eye = landmarks['right_eye']
                left_ear = eye_aspect_ratio(left_eye)
                right_ear = eye_aspect_ratio(right_eye)

                # Determine if eyes are open or closed based on the EAR threshold
                ear_threshold = 0.2
                left_eye_state = "Open" if left_ear > ear_threshold else "Closed"
                right_eye_state = "Open" if right_ear > ear_threshold else "Closed"

                # Inside the main loop, after detecting cheating incidents
                head_position_changes = 0  # Placeholder, adjust as needed
                cheating_incident = "Yes" if head_movement_angle > cheating_threshold or left_eye_state == "Closed" or right_eye_state == "Closed" or head_position_changes > cheating_threshold else "No"

                # Continuous talking check
                if name != "No person":
                    if talk_start_time is None:
                        talk_start_time = time.time()
                    else:
                        talk_duration = time.time() - talk_start_time
                        if talk_duration >= talk_duration_threshold:
                            cheating_incident = "Yes (Continuous Talking)"
                else:
                    talk_start_time = None

                # Check if face disappears from the frame
                if name != "No person":
                    person_detected[name] = True
                    if name not in face_disappearance_warnings:
                        face_disappearance_warnings[name] = 0
                    else:
                        face_disappearance_warnings[name] += 1
                        if face_disappearance_warnings[name] >= frame_count_to_warn:
                            print(f"WARNING: {name} has disappeared from the window.")
                            markAttendance(name, 0, "N/A", "N/A", "N/A", "Face Disappeared")
                            del face_disappearance_warnings[name]
                else:
                    for name, detected in person_detected.items():
                        if detected:
                            if name not in person_movement_warnings:
                                person_movement_warnings[name] = 0
                            else:
                                person_movement_warnings[name] += 1
                                if person_movement_warnings[name] >= movement_warning_threshold:
                                    print(f"WARNING: {name} has moved away from the window.")
                                    markAttendance(name, 0, "N/A", "N/A", "N/A", "Moved Away from Window")
                                    del person_movement_warnings[name]
                    person_detected = {name: False for name in person_detected.keys()}
                    if name in face_disappearance_warnings:
                        del face_disappearance_warnings[name]

                # Drawing logic
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'{name} - Head Movement: {head_movement_angle:.2f} degrees, Left Eye: {left_eye_state}, Right Eye: {right_eye_state}', (x1 + 6, y2 - 5),
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)

                # Mark attendance with head position and cheating incident
                markAttendance(name, head_movement_angle, left_eye_state, right_eye_state, head_position, cheating_incident)

                # Draw text indicating head position on the frame
                cv2.putText(img, f'Head Position: {head_position}', (x1 + 6, y1 - 15), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)

    # Display the image
    cv2.imshow('webcam', img)

    # After processing (inside your loop, right before `cv2.imshow`):
    # Inside the main loop, after writing attendance records
    current_time = time.time()
    if current_time - last_written_time >= write_interval:
        write_attendance_to_csv(attendance_records)
        last_written_time = current_time

    # Check for 'q' key press to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
