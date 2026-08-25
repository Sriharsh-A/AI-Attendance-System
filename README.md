# AI Attendance System

An AI-powered attendance management system that uses face recognition to automatically identify registered students and record their attendance.

The system captures faces through a webcam, compares them with previously generated face encodings, identifies the student, and stores the attendance record with the date and time.

---

## 📌 Project Overview

Traditional attendance systems require manual marking, which can be time-consuming and prone to errors.

This project implements an automated attendance system using computer vision and face recognition. Registered student faces are converted into numerical face encodings and stored locally. During attendance, the webcam captures live video, detects faces, compares them with the stored encodings, and marks recognized students as present.

The system also provides a graphical user interface for starting attendance, registering students, updating face encodings, and viewing attendance records.

---

## ✨ Features

- Real-time face detection
- Face recognition using facial encodings
- Webcam-based attendance
- Automatic student identification
- Automatic attendance marking
- Date and time recording
- Prevention of duplicate attendance on the same day
- Support for multiple registered students
- Unknown face detection
- CSV-based attendance storage
- Graphical user interface using Tkinter
- Face registration and encoding management

---

## 🧠 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| OpenCV | Webcam access and image processing |
| face_recognition | Face detection and recognition |
| dlib | Face recognition backend |
| NumPy | Numerical operations |
| Tkinter | Graphical user interface |
| scikit-learn | LFW sample face dataset |
| CSV | Attendance data storage |
| Pickle | Face encoding storage |

---

## 🏗️ System Architecture

```text
                ┌─────────────────────┐
                │     USB Webcam      │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   Face Detection    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Generate Face       │
                │ Encoding            │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Compare with Stored │
                │ Face Encodings      │
                └──────────┬──────────┘
                           │
                    ┌──────┴──────┐
                    │             │
                    ▼             ▼
               Recognized      Unknown
                    │
                    ▼
             Mark Attendance
                    │
                    ▼
             attendance.csv

📂 Project Structure
AI_Attendance_System/
│
├── src/
│   ├── app.py
│   ├── attendance.py
│   ├── register.py
│   ├── encode_faces.py
│   └── test_camera.py
│
├── dataset/
│   └── Student face images
│
├── encodings/
│   └── encodings.pkl
│
├── attendance/
│   └── attendance.csv
│
├── .gitignore
├── requirements.txt
└── README.md
Important

The following files/folders are intentionally excluded from the GitHub repository:

venv/
Student face images
Generated face encodings
Attendance records

This is handled using .gitignore to avoid exposing personal biometric data and locally generated records.

⚙️ Installation
1. Clone the repository
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd AI-Attendance-System
2. Create a virtual environment
python -m venv venv
3. Activate the virtual environment
Windows PowerShell
.\venv\Scripts\Activate.ps1
4. Install dependencies
pip install -r requirements.txt
▶️ Running the Application

Start the graphical interface:

python src/app.py

The application provides options to:

Start Attendance
Register Student
Update Face Encodings
View Attendance
Exit
👤 Registering a Student

Run the registration process through the application or directly using:

python src/register.py

The system captures multiple face images for the student and stores them locally in the dataset/ directory.

Each student is represented using multiple face samples to improve recognition reliability.

🧠 Generating Face Encodings

After registering students, generate their face encodings:

python src/encode_faces.py

The system:

Reads the registered face images.
Detects faces.
Generates facial encodings.
Associates each encoding with the corresponding student.
Saves the resulting data to:
encodings/encodings.pkl
📷 Starting Attendance

The attendance system can be started directly using:

python src/attendance.py

The system uses the connected USB webcam to capture live video.

For each detected face:

The face is detected.
A face encoding is generated.
The encoding is compared with stored encodings.
The closest matching registered student is identified.
The student's name is displayed.
Attendance is recorded if the student has not already been marked present that day.

Press:

Q

to close the camera window.

📊 Attendance Records

Attendance is stored in:

attendance/attendance.csv

The CSV contains:

Name,Date,Time,Status

Example:

Harsh,2026-08-25,14:25:48,Present

The system prevents the same student from being recorded multiple times on the same day.

🔍 Face Recognition

The project uses facial encodings rather than directly comparing image pixels.

A registered face is converted into a numerical representation. During live attendance, the detected face is converted into another encoding and compared against the stored encodings.

A matching face is assigned the corresponding registered student's name.

Faces that do not sufficiently match a registered student are treated as:

Unknown

and are not marked present.

🖥️ Graphical User Interface

The project includes a Tkinter-based graphical interface with the following options:

AI ATTENDANCE SYSTEM

📷 Start Attendance
👤 Register Student
🔄 Update Face Encodings
📊 View Attendance
❌ Exit

The interface provides a simple way to operate the complete attendance workflow without manually running every Python script.

🔐 Privacy Considerations

Face images and generated face encodings are locally stored and are not included in the public GitHub repository.

Attendance records are also excluded from version control.

The .gitignore file prevents these files from being accidentally committed.

🚀 Future Enhancements

Possible improvements include:

Database integration using MySQL or SQLite
Admin authentication
Student management dashboard
Attendance reports and analytics
Export attendance to Excel/PDF
Email notifications
Cloud-based storage
Improved recognition under different lighting conditions
Liveness detection to reduce spoofing
Mobile or web-based interface
🎯 Project Objective

The objective of this project is to develop an automated attendance management system using face recognition that reduces manual effort, identifies registered students through a webcam, records attendance automatically, and maintains organized attendance records.

👨‍💻 Author

Sriharsh Akkala

AI Attendance System — Major Project
