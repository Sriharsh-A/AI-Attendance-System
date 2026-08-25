import cv2
import face_recognition
import pickle
import os
import csv
from datetime import datetime

# -----------------------------
# SETTINGS
# -----------------------------

CAMERA_INDEX = 1
ENCODINGS_FILE = "encodings/encodings.pkl"
ATTENDANCE_FILE = "attendance/attendance.csv"

# -----------------------------
# CREATE ATTENDANCE FOLDER
# -----------------------------

os.makedirs("attendance", exist_ok=True)

# -----------------------------
# LOAD FACE ENCODINGS
# -----------------------------

if not os.path.exists(ENCODINGS_FILE):
    print("❌ Encodings file not found.")
    print("Run encode_faces.py first.")
    exit()

with open(ENCODINGS_FILE, "rb") as file:
    data = pickle.load(file)

known_encodings = data["encodings"]
known_names = data["names"]

print(f"✅ Loaded {len(known_encodings)} face encodings.")

# -----------------------------
# CREATE CSV FILE
# -----------------------------

if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Date", "Time", "Status"])

# -----------------------------
# ATTENDANCE FUNCTION
# -----------------------------

def mark_attendance(name):

    today = datetime.now().strftime("%Y-%m-%d")

    # Check if student already marked today
    with open(ATTENDANCE_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["Name"] == name and row["Date"] == today:
                return False

    current_time = datetime.now().strftime("%H:%M:%S")

    with open(ATTENDANCE_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            name,
            today,
            current_time,
            "Present"
        ])

    print(f"✅ Attendance marked: {name}")

    return True


# -----------------------------
# START CAMERA
# -----------------------------

camera = cv2.VideoCapture(
    CAMERA_INDEX,
    cv2.CAP_DSHOW
)

if not camera.isOpened():
    print("❌ Could not open USB webcam.")
    exit()

print("\n📷 Attendance system started.")
print("Press Q to exit.\n")

while True:

    ret, frame = camera.read()

    if not ret:
        print("❌ Could not read camera frame.")
        break

    # Resize frame for faster processing
    small_frame = cv2.resize(
        frame,
        (0, 0),
        fx=0.25,
        fy=0.25
    )

    # Convert BGR → RGB
    rgb_small_frame = cv2.cvtColor(
        small_frame,
        cv2.COLOR_BGR2RGB
    )

    # Detect faces
    face_locations = face_recognition.face_locations(
        rgb_small_frame
    )

    # Generate encodings
    face_encodings = face_recognition.face_encodings(
        rgb_small_frame,
        face_locations
    )

    # Process each detected face
    for face_encoding, face_location in zip(
        face_encodings,
        face_locations
    ):

        matches = face_recognition.compare_faces(
            known_encodings,
            face_encoding,
            tolerance=0.5
        )

        name = "Unknown"

        if True in matches:

            face_distances = face_recognition.face_distance(
                known_encodings,
                face_encoding
            )

            best_match_index = face_distances.argmin()

            if matches[best_match_index]:
                name = known_names[best_match_index]

                mark_attendance(name)

        # Scale coordinates back to original frame
        top, right, bottom, left = face_location

        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw rectangle
        cv2.rectangle(
            frame,
            (left, top),
            (right, bottom),
            (0, 255, 0),
            2
        )

        # Draw name
        cv2.rectangle(
            frame,
            (left, bottom - 35),
            (right, bottom),
            (0, 255, 0),
            cv2.FILLED
        )

        cv2.putText(
            frame,
            name,
            (left + 6, bottom - 6),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 0),
            2
        )

    # Display camera
    cv2.imshow(
        "AI Attendance System",
        frame
    )

    # Quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()

print("\n👋 Attendance system closed.")