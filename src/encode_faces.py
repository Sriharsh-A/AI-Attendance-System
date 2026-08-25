import os
import pickle
import face_recognition

DATASET_DIR = "dataset"
ENCODINGS_DIR = "encodings"
ENCODINGS_FILE = os.path.join(ENCODINGS_DIR, "encodings.pkl")

os.makedirs(ENCODINGS_DIR, exist_ok=True)

known_encodings = []
known_names = []

print("🔍 Starting face encoding...\n")

for filename in os.listdir(DATASET_DIR):

    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    image_path = os.path.join(DATASET_DIR, filename)

    # Extract student name from filename
    name = os.path.splitext(filename)[0]

    # Remove image number from names like:
    # Sriharsh_1 → Sriharsh
    if "_" in name:
        name = name.rsplit("_", 1)[0]

    print(f"Processing: {filename}")

    # Load image
    image = face_recognition.load_image_file(image_path)

    # Detect faces
    face_locations = face_recognition.face_locations(image)

    if len(face_locations) == 0:
        print("   ❌ No face detected. Skipping.")
        continue

    if len(face_locations) > 1:
        print("   ❌ Multiple faces detected. Skipping.")
        continue

    # Generate face encoding
    encodings = face_recognition.face_encodings(
        image,
        face_locations
    )

    if len(encodings) == 0:
        print("   ❌ Could not generate encoding.")
        continue

    known_encodings.append(encodings[0])
    known_names.append(name)

    print(f"   ✅ Encoding created for {name}")

# Save encodings
data = {
    "encodings": known_encodings,
    "names": known_names
}

with open(ENCODINGS_FILE, "wb") as file:
    pickle.dump(data, file)

print("\n" + "=" * 50)
print("🎉 FACE ENCODING COMPLETED")
print("=" * 50)
print(f"Students encoded: {len(set(known_names))}")
print(f"Total face encodings: {len(known_encodings)}")
print(f"Saved to: {ENCODINGS_FILE}")