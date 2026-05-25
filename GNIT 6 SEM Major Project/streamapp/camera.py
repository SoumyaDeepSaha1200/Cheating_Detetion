import cv2
import face_recognition
import numpy as np
import os
import datetime
import dlib
from imutils.video import VideoStream
import time
from .models import AttendanceRecord
from django.core.files.base import ContentFile
import csv
import random
import string
import speech_recognition as sr
import audioop

class VideoCamera:
    def __init__(self):
        self.cap = VideoStream(src=0).start()
        self.images = []
        self.classNames = []
        self.attendance_records = {}
        self.write_interval = 10
        self.last_written_time = time.time()
        self.warnings = {}
        self.warning_threshold = 10
        self.frame_count_to_warn = 30
        self.face_disappearance_warnings = {}
        self.person_detected = {}
        self.person_movement_warnings = {}
        self.movement_warning_threshold = 30
        self.cheating_threshold = 10
        self.start_time = time.time()
        self.mouth_moving = False
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.recognizer = sr.Recognizer()

        path = 'student_images'
        mylist = os.listdir(path)
        for cl in mylist:
            curImg = cv2.imread(os.path.join(path, cl))
            self.images.append(curImg)
            self.classNames.append(os.path.splitext(cl)[0])

        self.encoded_face_train = self.findEncodings(self.images)
        self.detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks_GTX.dat")

    


    # Uniqu
    # e id generate from here 
    def generate_unique_id(self):
        # Generate a random unique ID of length 8
        unique_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return unique_id


    def background_sound_detection(self):
        # Use the default microphone as the audio source
        with self.microphone as source:
        # Adjust recognizer sensitivity to help recognize speech better in noisy environments
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Ready to detect background noise. Listening...")

        # Attempt to listen to the source, with specified timeouts
            try:
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=1)
            except sr.WaitTimeoutError:
                print("No speech was detected within the allowed time.")
                return "No"  # Return "No" if no speech detected
            except Exception as e:
                print(f"An error occurred while listening: {e}")
                return None

            # Print audio data for debugging
            print(f"Audio data captured: {audio}")

        # Optional: Recognize speech using Google's free web service
        try:
            # Recognize speech using Google's free web service
            text = self.recognizer.recognize_google(audio)
            print(f"Google Speech Recognition thinks you said: {text}")
            return "Yes"  # Return "Yes" if speech is detected
        except sr.UnknownValueError:
            print("Could not understand audio. Please speak clearly and try again.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

        return "No"  # Return "No" if speech is not detected



    def background_noise_detection(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Ready to detect background noise level. Listening...")

            try:
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=1)
                rms = audioop.rms(audio.frame_data, 2)
                noise_level = "High" if rms > 1000 else "Low"  # You may adjust the threshold
                return noise_level
            except sr.WaitTimeoutError:
                print("No noise was detected within the allowed time.")
                return "Unknown"
            except Exception as e:
                print(f"An error occurred while listening: {e}")
                return "Unknown"

    
    








    def write_attendance_to_csv(self):
        if not self.attendance_records:
            return

        with open('output.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(["Name", "SessionID", "StudentID", "SuspiciousObject", "SoundDetection", "MultiplePersons", "BackgroundNoiseLevel", "Date", "Time", "Cheating Incident", "Head Movement", "Left Eye", "Right Eye", "Head Position"])

            for record in self.attendance_records.values():
                writer.writerow([
                    record.get("Name", ""),
                    record.get("SessionID", ""),
                    record.get("StudentID", ""),
                    record.get("SuspiciousObject", ""),
                    record.get("SoundDetection", ""),
                    record.get("MultiplePersons", ""),
                    record.get("BackgroundNoiseLevel", ""),
                    record.get("Date", ""),
                    record.get("Time", ""),
                    record.get("Cheating Incident", ""),
                    record.get("Head Movement", ""),
                    record.get("Left Eye", ""),
                    record.get("Right Eye", ""),
                    record.get("Head Position", ""),
                ])

        if writer is not None:
            file.close()







    def markAttendance(self, name, head_movement_angle, left_eye_state, right_eye_state, head_position, cheating_incident=None):
        now = datetime.datetime.now()
        date = now.date()
        time_str = now.time()

        sound_detection_result = self.background_sound_detection()
        background_noise_level = self.background_noise_detection()

        if cheating_incident == "Yes":
            img_data = self.cap.read()
            ret, img_data_jpeg = cv2.imencode('.jpg', img_data)
            img_data_bytes = img_data_jpeg.tobytes()

            record = AttendanceRecord.objects.create(
                name=name,
                head_movement=head_movement_angle,
                left_eye=left_eye_state,
                right_eye=right_eye_state,
                head_position=head_position,
                date=date,
                time=time_str,
                cheating_incident=cheating_incident,
                sound_detection=sound_detection_result,
                background_noise_level=background_noise_level,
            )

            image_filename = f'{name}_{date}_{time_str}.jpg'
            content = ContentFile(img_data_bytes)
            record.image_path.save(image_filename, content, save=True)
        else:
            record = AttendanceRecord.objects.create(
                name=name,
                head_movement=head_movement_angle,
                left_eye=left_eye_state,
                right_eye=right_eye_state,
                head_position=head_position,
                date=date,
                time=time_str,
                cheating_incident=cheating_incident,
                sound_detection=sound_detection_result,
                background_noise_level=background_noise_level,
            )

        if name not in self.attendance_records or (time.time() - self.attendance_records[name]["Last Marked"]) >= 10:
            self.attendance_records[name] = {
                "Name": name,
                "SessionID": self.generate_unique_id(),
                "StudentID": self.generate_unique_id(),
                "SuspiciousObject": "N/A",
                "SoundDetection": sound_detection_result,
                "MultiplePersons": "N/A",
                "BackgroundNoiseLevel": background_noise_level,
                "Head Movement": f"{head_movement_angle:.2f} degrees" if name != "No person" else head_movement_angle,
                "Left Eye": left_eye_state,
                "Right Eye": right_eye_state,
                "Head Position": head_position,
                "Date": date,
                "Time": time_str,
                "Cheating Incident": cheating_incident,
                "Last Marked": time.time()
            }
            self.warnings[name] = 0
        else:
            self.warnings[name] += 1
        if self.warnings[name] >= self.warning_threshold:
            del self.attendance_records[name]
            del self.warnings[name]

        self.write_attendance_to_csv()











    def angle_between_points(self, p1, p2):
        # Calculate angle in radians
        angle_radians = np.arctan2(p2[1] - p1[1], p2[0] - p1[0])
        # Convert to degrees
        angle_degrees = np.degrees(angle_radians)
        return angle_degrees






    def calculate_head_movement_angle(self, landmarks):
        # Extract relevant landmarks for head movement calculation
        left_eye_center = np.mean(landmarks['left_eye'], axis=0)
        right_eye_center = np.mean(landmarks['right_eye'], axis=0)

        # Calculate the head movement angle
        head_movement_angle = self.angle_between_points(left_eye_center, right_eye_center)

        return head_movement_angle








    def eye_aspect_ratio(self, eye):
        # Calculate the Euclidean distances between the vertical eye landmarks
        vertical_dist1 = np.linalg.norm(np.array(eye[1]) - np.array(eye[5]))
        vertical_dist2 = np.linalg.norm(np.array(eye[2]) - np.array(eye[4]))

        # Calculate the Euclidean distance between the horizontal eye landmarks
        horizontal_dist = np.linalg.norm(np.array(eye[0]) - np.array(eye[3]))

        # Calculate the eye aspect ratio
        ear = (vertical_dist1 + vertical_dist2) / (2.0 * horizontal_dist)

        return ear








    

    def determine_head_position(self, landmarks):
        nose_point = landmarks['nose_bridge'][3]  
        chin_point = landmarks['chin'][8]  

        if chin_point[0] == nose_point[0]:
            return "Not Moving"

        slope = (chin_point[1] - nose_point[1]) / (chin_point[0] - nose_point[0])

        angle = np.degrees(np.arctan(slope))

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
        

    



    def detect_suspicious_objects(self, img):
        # This function should be implemented to detect suspicious objects
        # Placeholder for object detection code
        pass

    

    def detect_multiple_persons(self, img):
        # This function should be implemented to detect multiple persons in the frame
        # Placeholder for multiple persons detection code
        pass











    def face_cheating_detection(self):
        img = self.cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faces_in_frame = face_recognition.face_locations(imgS)
        encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)

        if not faces_in_frame:
            #print("No person in the screen.")
            for name in self.person_detected.keys():
                self.person_detected[name] = False
                self.markAttendance("No person", 0, "N/A", "N/A", "N/A")

        else:
            for encode_face, faceloc in zip(encoded_faces, faces_in_frame):
                name = "Unknown"
                matches = face_recognition.compare_faces(self.encoded_face_train, encode_face)
                faceDist = face_recognition.face_distance(self.encoded_face_train, encode_face)
                matchIndex = np.argmin(faceDist)

                if matches[matchIndex]:
                    name = self.classNames[matchIndex].upper().lower()
                    y1, x2, y2, x1 = faceloc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    landmarks = face_recognition.face_landmarks(imgS, [faceloc])[0]
                    head_movement_angle = self.calculate_head_movement_angle(landmarks)
                    head_position = self.determine_head_position(landmarks)

                    left_eye = landmarks['left_eye']
                    right_eye = landmarks['right_eye']
                    left_ear = self.eye_aspect_ratio(left_eye)
                    right_ear = self.eye_aspect_ratio(right_eye)

                    ear_threshold = 0.2
                    left_eye_state = "Open" if left_ear > ear_threshold else "Closed"
                    right_eye_state = "Open" if right_ear > ear_threshold else "Closed"

                    head_position_changes = 0
                    cheating_incident = "Yes" if head_movement_angle > self.cheating_threshold or left_eye_state == "Closed" or right_eye_state == "Closed" or head_position_changes > self.cheating_threshold else "No"

                    if name != "No person":
                        if name not in self.face_disappearance_warnings:
                            self.face_disappearance_warnings[name] = 0
                        else:
                            self.face_disappearance_warnings[name] += 1
                            if self.face_disappearance_warnings[name] >= self.frame_count_to_warn:
                                #print(f"WARNING: {name} has disappeared from the window.")
                                self.markAttendance(name, 0, "N/A", "N/A", "N/A", "Face Disappeared")
                                del self.face_disappearance_warnings[name]
                    else:
                        for name, detected in self.person_detected.items():
                            if detected:
                                if name not in self.person_movement_warnings:
                                    self.person_movement_warnings[name] = 0
                                else:
                                    self.person_movement_warnings[name] += 1
                                    if self.person_movement_warnings[name] >= self.movement_warning_threshold:
                                        #print(f"WARNING: {name} has moved away from the window.")
                                        self.markAttendance(name, 0, "N/A", "N/A", "N/A", "Moved Away from Window")
                                        del self.person_movement_warnings[name]
                        self.person_detected = {name: False for name in self.person_detected.keys()}
                        if name in self.face_disappearance_warnings:
                            del self.face_disappearance_warnings[name]

                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f'{name} - Head Movement: {head_movement_angle:.2f} degrees, Left Eye: {left_eye_state}, Right Eye: {right_eye_state}', (x1 + 6, y2 - 5),
                                cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)

                    self.markAttendance(name, head_movement_angle, left_eye_state, right_eye_state, head_position, cheating_incident)

                    cv2.putText(img, f'Head Position: {head_position}', (x1 + 6, y1 - 15), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
                    
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()









    def findEncodings(self, images):
        encodedList = []
        for img in images:
            imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(imgS)[0]
            encodedList.append(encode)
        return encodedList
    

    
    



    

