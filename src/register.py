import cv2
import face_recognition
import os
import re

# Camera index for external USB webcam
CAMERA_INDEX = 1

# Number of face images to capture
NUM_IMAGES = 5

# Create dataset folder
os.makedirs("dataset", exist_ok=True)

name = input("Enter student name: ").strip()

if not name:
    print("❌ Name cannot be empty.")
    exit()

# Make the name safe for filenames
safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", name)

camera = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)

if not camera.isOpened():
    print("❌ Could not open USB webcam.")
    exit()

print("\n📷 USB webcam started.")
print("Position your face clearly in front of the camera.")
print("Press SPACE to capture a face.")
print("Press Q to quit.\n")

count = 0

while count < NUM_IMAGES:

    ret, frame = camera.read()

    if not ret:
        print("❌ Could not read camera frame.")
        break

    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces
    face_locations = face_recognition.face_locations(rgb_frame)

    # Draw rectangles around detected faces
    for top, right, bottom, left in face_locations:
        cv2.rectangle(
            frame,
            (left, top),
            (right, bottom),
            (0, 255, 0),
            2
        )

    cv2.putText(
        frame,
        f"Captured: {count}/{NUM_IMAGES}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Student Registration", frame)

    key = cv2.waitKey(1) & 0xFF

    # Capture image
    if key == ord(" "):

        if len(face_locations) == 0:
            print("❌ No face detected. Try again.")

        elif len(face_locations) > 1:
            print("❌ Multiple faces detected. Only one student should be visible.")

        else:
            top, right, bottom, left = face_locations[0]

            # Crop the detected face
            face_image = frame[top:bottom, left:right]

            if face_image.size == 0:
                print("❌ Invalid face image.")
                continue

            filename = f"dataset/{safe_name}_{count + 1}.jpg"

            cv2.imwrite(filename, face_image)

            count += 1

            print(f"✅ Face image {count}/{NUM_IMAGES} saved: {filename}")

    elif key == ord("q"):
        print("\n❌ Registration cancelled.")
        break

camera.release()
cv2.destroyAllWindows()

if count == NUM_IMAGES:
    print(f"\n🎉 Registration completed for {name}!")
    print(f"Saved {NUM_IMAGES} face images in the dataset folder.")