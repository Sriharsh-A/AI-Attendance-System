import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import csv
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REGISTER_SCRIPT = os.path.join(BASE_DIR, "src", "register.py")
ENCODE_SCRIPT = os.path.join(BASE_DIR, "src", "encode_faces.py")
ATTENDANCE_SCRIPT = os.path.join(BASE_DIR, "src", "attendance.py")
ATTENDANCE_FILE = os.path.join(
    BASE_DIR,
    "attendance",
    "attendance.csv"
)

BG = "#f4f7fb"
CARD = "#ffffff"
PRIMARY = "#2563eb"
TEXT = "#172033"
SECONDARY = "#64748b"
SUCCESS = "#16a34a"
BORDER = "#e2e8f0"


def start_attendance():
    try:
        subprocess.Popen(
            [sys.executable, ATTENDANCE_SCRIPT],
            cwd=BASE_DIR
        )

        status_label.config(
            text="● Attendance system running",
            fg=SUCCESS
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Could not start attendance system.\n\n{e}"
        )


def register_student():
    try:
        subprocess.run(
            [sys.executable, REGISTER_SCRIPT],
            cwd=BASE_DIR
        )

        result = messagebox.askyesno(
            "Registration",
            "Registration process completed.\n\n"
            "Do you want to update face encodings now?"
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
                "Face encodings updated successfully."
            )
        else:
            messagebox.showerror(
                "Encoding Error",
                "Face encoding process failed."
            )

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Could not update face encodings.\n\n{e}"
        )


def view_attendance():
    window = tk.Toplevel(root)
    window.title("Attendance Records")
    window.geometry("800x500")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="Attendance Records",
        font=("Segoe UI", 22, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(pady=(25, 5))

    tk.Label(
        window,
        text=datetime.now().strftime("%A, %d %B %Y"),
        font=("Segoe UI", 11),
        bg=BG,
        fg=SECONDARY
    ).pack(pady=(0, 20))

    table_frame = tk.Frame(
        window,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    table_frame.pack(
        padx=30,
        pady=5,
        fill="both",
        expand=True
    )

    columns = ("Name", "Date", "Time", "Status")

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:
        table.heading(column, text=column)
        table.column(
            column,
            anchor="center",
            width=170
        )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=table.yview
    )

    table.configure(
        yscrollcommand=scrollbar.set
    )

    table.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(10, 0),
        pady=10
    )

    scrollbar.pack(
        side="right",
        fill="y",
        pady=10
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
                f"Could not read attendance records.\n\n{e}"
            )
    else:
        messagebox.showinfo(
            "No Records",
            "No attendance records found."
        )


def exit_application():
    status_label.config(
        text="● Application closed",
        fg="#dc2626"
    )

    root.after(
        300,
        root.destroy
    )


root = tk.Tk()

root.title("AI Attendance System")
root.geometry("700x720")
root.resizable(False, False)
root.configure(bg=BG)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=CARD,
    foreground=TEXT,
    rowheight=35,
    fieldbackground=CARD,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background="#eaf0f7",
    foreground=TEXT,
    font=("Segoe UI", 10, "bold")
)

style.map(
    "Treeview",
    background=[("selected", "#dbeafe")],
    foreground=[("selected", TEXT)]
)

header = tk.Frame(
    root,
    bg=PRIMARY,
    height=175
)

header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="AI ATTENDANCE SYSTEM",
    font=("Segoe UI", 27, "bold"),
    bg=PRIMARY,
    fg="white"
).pack(pady=(35, 5))

tk.Label(
    header,
    text="Face Recognition Based Attendance Management",
    font=("Segoe UI", 12),
    bg=PRIMARY,
    fg="#dbeafe"
).pack()

status_label = tk.Label(
    root,
    text="● System ready",
    font=("Segoe UI", 11, "bold"),
    bg=BG,
    fg=SUCCESS
)

status_label.pack(pady=(25, 5))

date_label = tk.Label(
    root,
    text=datetime.now().strftime("%d %B %Y"),
    font=("Segoe UI", 10),
    bg=BG,
    fg=SECONDARY
)

date_label.pack(pady=(0, 20))


def create_button(text, command):
    button = tk.Button(
        root,
        text=text,
        command=command,
        font=("Segoe UI", 12, "bold"),
        bg=CARD,
        fg=TEXT,
        activebackground="#eaf0ff",
        activeforeground=PRIMARY,
        relief="flat",
        bd=0,
        width=32,
        height=2,
        cursor="hand2",
        highlightbackground=BORDER,
        highlightthickness=1
    )

    button.pack(pady=7)

    return button


create_button(
    "📷   Start Attendance",
    start_attendance
)

create_button(
    "👤   Register Student",
    register_student
)

create_button(
    "🔄   Update Face Encodings",
    encode_faces
)

create_button(
    "📊   View Attendance",
    view_attendance
)

create_button(
    "❌   Exit",
    exit_application
)

info_card = tk.Frame(
    root,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)

info_card.pack(
    padx=80,
    pady=(25, 10),
    fill="x"
)

tk.Label(
    info_card,
    text="System Information",
    font=("Segoe UI", 11, "bold"),
    bg=CARD,
    fg=TEXT
).pack(pady=(12, 5))

tk.Label(
    info_card,
    text="Real-time face recognition • Automated attendance • CSV storage",
    font=("Segoe UI", 9),
    bg=CARD,
    fg=SECONDARY
).pack(pady=(0, 12))

tk.Label(
    root,
    text="Major Project • AI Attendance System",
    font=("Segoe UI", 9),
    bg=BG,
    fg="#94a3b8"
).pack(
    side="bottom",
    pady=18
)

root.mainloop()