import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import csv


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REGISTER_SCRIPT = os.path.join(BASE_DIR, "src", "register.py")
ENCODE_SCRIPT = os.path.join(BASE_DIR, "src", "encode_faces.py")
ATTENDANCE_SCRIPT = os.path.join(BASE_DIR, "src", "attendance.py")
ATTENDANCE_FILE = os.path.join(BASE_DIR, "attendance", "attendance.csv")


# --------------------------------------------------
# COLORS
# --------------------------------------------------

BG_COLOR = "#f4f6f8"
TITLE_COLOR = "#1f2937"
BUTTON_COLOR = "#2563eb"
TEXT_COLOR = "#ffffff"


# --------------------------------------------------
# FUNCTIONS
# --------------------------------------------------

def start_attendance():
    try:
        subprocess.Popen(
            [sys.executable, ATTENDANCE_SCRIPT],
            cwd=BASE_DIR
        )
    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Could not start attendance system.\n\n{e}"
        )


def register_student():
    try:
        process = subprocess.run(
            [sys.executable, REGISTER_SCRIPT],
            cwd=BASE_DIR
        )

        if process.returncode == 0:
            result = messagebox.askyesno(
                "Registration Complete",
                "Student registration finished.\n\n"
                "Do you want to update the face encodings now?"
            )

            if result:
                encode_faces()

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Could not register student.\n\n{e}"
        )


def encode_faces():
    try:
        process = subprocess.run(
            [sys.executable, ENCODE_SCRIPT],
            cwd=BASE_DIR
        )

        if process.returncode == 0:
            messagebox.showinfo(
                "Success",
                "Face encodings updated successfully!"
            )
        else:
            messagebox.showerror(
                "Error",
                "Face encoding process failed."
            )

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Could not encode faces.\n\n{e}"
        )


def view_attendance():
    window = tk.Toplevel(root)
    window.title("Attendance Records")
    window.geometry("700x450")
    window.configure(bg=BG_COLOR)

    title = tk.Label(
        window,
        text="Attendance Records",
        font=("Segoe UI", 20, "bold"),
        bg=BG_COLOR,
        fg=TITLE_COLOR
    )
    title.pack(pady=20)

    columns = ("Name", "Date", "Time", "Status")

    table = ttk.Treeview(
        window,
        columns=columns,
        show="headings",
        height=14
    )

    for column in columns:
        table.heading(column, text=column)
        table.column(column, width=150, anchor="center")

    table.pack(
        padx=20,
        pady=10,
        fill="both",
        expand=True
    )

    if os.path.exists(ATTENDANCE_FILE):

        try:
            with open(
                ATTENDANCE_FILE,
                "r",
                newline="",
                encoding="utf-8"
            ) as file:

                reader = csv.DictReader(file)

                for row in reader:
                    table.insert(
                        "",
                        "end",
                        values=(
                            row["Name"],
                            row["Date"],
                            row["Time"],
                            row["Status"]
                        )
                    )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not read attendance file.\n\n{e}"
            )

    else:
        messagebox.showinfo(
            "No Records",
            "No attendance records found."
        )


def exit_application():
    root.destroy()


# --------------------------------------------------
# MAIN WINDOW
# --------------------------------------------------

root = tk.Tk()

root.title("AI Attendance System")
root.geometry("600x650")
root.resizable(False, False)
root.configure(bg=BG_COLOR)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

title = tk.Label(
    root,
    text="AI ATTENDANCE SYSTEM",
    font=("Segoe UI", 26, "bold"),
    bg=BG_COLOR,
    fg=TITLE_COLOR
)

title.pack(pady=(50, 5))


subtitle = tk.Label(
    root,
    text="Face Recognition Based Attendance",
    font=("Segoe UI", 13),
    bg=BG_COLOR,
    fg="#6b7280"
)

subtitle.pack(pady=(0, 40))


# --------------------------------------------------
# BUTTON FUNCTION
# --------------------------------------------------

def create_button(text, command):

    button = tk.Button(
        root,
        text=text,
        command=command,
        font=("Segoe UI", 13, "bold"),
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        activebackground="#1d4ed8",
        activeforeground=TEXT_COLOR,
        relief="flat",
        width=28,
        height=2,
        cursor="hand2"
    )

    button.pack(pady=10)

    return button


# --------------------------------------------------
# BUTTONS
# --------------------------------------------------

create_button(
    "📷  Start Attendance",
    start_attendance
)

create_button(
    "👤  Register Student",
    register_student
)

create_button(
    "🔄  Update Face Encodings",
    encode_faces
)

create_button(
    "📊  View Attendance",
    view_attendance
)

create_button(
    "❌  Exit",
    exit_application
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

footer = tk.Label(
    root,
    text="AI • Face Recognition • Automated Attendance",
    font=("Segoe UI", 9),
    bg=BG_COLOR,
    fg="#9ca3af"
)

footer.pack(side="bottom", pady=25)


# --------------------------------------------------
# START APPLICATION
# --------------------------------------------------

root.mainloop()