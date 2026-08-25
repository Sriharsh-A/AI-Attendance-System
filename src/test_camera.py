import cv2
import time

for index in range(3):
    print(f"\nTesting camera index {index}...")

    start = time.time()
    camera = cv2.VideoCapture(index, cv2.CAP_DSHOW)

    elapsed = time.time() - start

    if not camera.isOpened():
        print(f"❌ Index {index} unavailable ({elapsed:.2f}s)")
        camera.release()
        continue

    print(f"✅ Index {index} opened ({elapsed:.2f}s)")
    print("Press Q to close.")

    while True:
        ret, frame = camera.read()

        if not ret:
            print("❌ Could not read frame")
            break

        cv2.imshow(f"Camera Index {index}", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

print("\nDone.")