from sklearn.datasets import fetch_lfw_people
import os
import cv2

DATASET_DIR = "dataset"

os.makedirs(DATASET_DIR, exist_ok=True)

print("Downloading/loading LFW dataset...")
print("This may take a little while the first time.\n")

lfw = fetch_lfw_people(
    min_faces_per_person=20,
    color=True
)

print(f"Total images available: {len(lfw.images)}")

# Pick 3 identities that have enough images
selected_people = []

for person_id, name in enumerate(lfw.target_names):
    count = sum(lfw.target == person_id)

    if count >= 20:
        selected_people.append((person_id, name))

    if len(selected_people) == 3:
        break

print("\nSelected sample identities:")

for person_id, name in selected_people:
    print(f"- {name}")

# Save 5 images for each person
for person_id, name in selected_people:

    safe_name = name.replace(" ", "_")

    indices = [
        i for i, target in enumerate(lfw.target)
        if target == person_id
    ][:5]

    for number, index in enumerate(indices, start=1):

        image = lfw.images[index]

        # RGB → BGR for OpenCV
        # Convert float image (0-1) to uint8 (0-255)
        image = (image * 255).astype("uint8")

# RGB → BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        

        filename = f"{safe_name}_{number}.jpg"
        filepath = os.path.join(
            DATASET_DIR,
            filename
        )

        cv2.imwrite(filepath, image)

        print(f"Saved: {filepath}")

print("\n✅ Sample faces added successfully!")