import cv2

print("Opening USB Camera...")

camera = cv2.VideoCapture(2, cv2.CAP_DSHOW)

if not camera.isOpened():
    print("❌ USB Camera could not be opened")
    exit()

print("✅ USB Camera opened!")

while True:
    ret, frame = camera.read()

    if not ret:
        print("❌ Could not read frame")
        break

    cv2.imshow("USB Camera - AI Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()