from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("attendance.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll TEXT,
    name TEXT,
    student_class TEXT,
    section TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    roll TEXT,
    name TEXT,
    status TEXT,
    time TEXT
)
""")

conn.commit()

def login():

    user = username_entry.get()
    pwd = password_entry.get()

    if user == "admin" and pwd == "1234":
        login_window.destroy()
        main_app()
    else:
        error_label.config(text="Wrong Username or Password")

def main_app():

    global root
    root = Tk()

    root.title("School ERP Attendance System")
    root.geometry("1200x700")
    root.configure(bg="#0f172a")

    SIDEBAR = "#111827"
    BG = "#0f172a"
    CARD = "#1f2937"

    sidebar = Frame(root, bg=SIDEBAR, width=220)
    sidebar.pack(side=LEFT, fill=Y)

    main_area = Frame(root, bg=BG)
    main_area.pack(side=LEFT, fill=BOTH, expand=True)

    Label(sidebar,
          text="🏫 SCHOOL ERP",
          bg=SIDEBAR,
          fg="white",
          font=("Arial", 16, "bold")).pack(pady=20)

    Label(main_area,
          text="Student Registration & Attendance",
          bg=BG,
          fg="white",
          font=("Arial", 20, "bold")).pack(pady=10)

    card_frame = Frame(main_area, bg=BG)
    card_frame.pack(pady=10)

    total_students_label = Label(card_frame,
                                 text="👨‍🎓 Students: 0",
                                 bg=CARD,
                                 fg="white",
                                 width=20,
                                 pady=15)

    present_label = Label(card_frame,
                          text="🟢 Present: 0",
                          bg=CARD,
                          fg="white",
                          width=20,
                          pady=15)

    absent_label = Label(card_frame,
                         text="🔴 Absent: 0",
                         bg=CARD,
                         fg="white",
                         width=20,
                         pady=15)

    total_students_label.pack(side=LEFT, padx=10)
    present_label.pack(side=LEFT, padx=10)
    absent_label.pack(side=LEFT, padx=10)

    form_frame = Frame(main_area, bg=BG)
    form_frame.pack(pady=10)

    Label(form_frame,
          text="Roll No",
          fg="white",
          bg=BG).grid(row=0, column=0, padx=5, pady=5)

    roll_entry = Entry(form_frame)
    roll_entry.grid(row=0, column=1, padx=5)

    Label(form_frame,
          text="Name",
          fg="white",
          bg=BG).grid(row=0, column=2, padx=5)

    name_entry = Entry(form_frame)
    name_entry.grid(row=0, column=3, padx=5)

    Label(form_frame,
          text="Class",
          fg="white",
          bg=BG).grid(row=1, column=0, padx=5)

    class_entry = Entry(form_frame)
    class_entry.grid(row=1, column=1, padx=5)

    Label(form_frame,
          text="Section",
          fg="white",
          bg=BG).grid(row=1, column=2, padx=5)

    section_entry = Entry(form_frame)
    section_entry.grid(row=1, column=3, padx=5)

    button_frame = Frame(main_area, bg=BG)
    button_frame.pack(pady=10)

    student_table_frame = Frame(main_area)
    student_table_frame.pack(pady=10)

    attendance_table_frame = Frame(main_area)
    attendance_table_frame.pack(pady=10)

    def update_dashboard():

        cur.execute("SELECT COUNT(*) FROM students")
        total_students = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM attendance WHERE status='Present'")
        total_present = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM attendance WHERE status='Absent'")
        total_absent = cur.fetchone()[0]

        total_students_label.config(text=f"👨‍🎓 Students: {total_students}")
        present_label.config(text=f"🟢 Present: {total_present}")
        absent_label.config(text=f"🔴 Absent: {total_absent}")

    def register_student():

        roll = roll_entry.get()
        name = name_entry.get()
        student_class = class_entry.get()
        section = section_entry.get()

        if roll == "" or name == "":
            messagebox.showerror("Error", "Please fill all required fields")
            return

        cur.execute("INSERT INTO students VALUES (?, ?, ?, ?)",
                    (roll, name, student_class, section))

        conn.commit()

        student_table.insert("", "end",
                             values=(roll, name, student_class, section))

        roll_entry.delete(0, END)
        name_entry.delete(0, END)
        class_entry.delete(0, END)
        section_entry.delete(0, END)

        update_dashboard()

    def mark_present():

        selected = student_table.selection()

        if not selected:
            messagebox.showwarning("Warning", "Select a student")
            return

        for item in selected:

            values = student_table.item(item)["values"]

            roll = values[0]
            name = values[1]

            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cur.execute("INSERT INTO attendance VALUES (?, ?, ?, ?)",
                        (roll, name, "Present", time))

            conn.commit()

            attendance_table.insert("", "end",
                                    values=(roll, name, "Present", time))

        update_dashboard()

    def mark_absent():

        selected = student_table.selection()

        if not selected:
            messagebox.showwarning("Warning", "Select a student")
            return

        for item in selected:

            values = student_table.item(item)["values"]

            roll = values[0]
            name = values[1]

            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cur.execute("INSERT INTO attendance VALUES (?, ?, ?, ?)",
                        (roll, name, "Absent", time))

            conn.commit()

            attendance_table.insert("", "end",
                                    values=(roll, name, "Absent", time))

        update_dashboard()

    def delete_student():

        selected = student_table.selection()

        if not selected:
            return

        for item in selected:

            values = student_table.item(item)["values"]

            cur.execute("DELETE FROM students WHERE roll=?", (values[0],))
            conn.commit()

            student_table.delete(item)

        update_dashboard()

    def clear_attendance():

        cur.execute("DELETE FROM attendance")
        conn.commit()

        for item in attendance_table.get_children():
            attendance_table.delete(item)

        update_dashboard()

    def show_graph():

        cur.execute("SELECT COUNT(*) FROM attendance WHERE status='Present'")
        present = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM attendance WHERE status='Absent'")
        absent = cur.fetchone()[0]

        plt.figure(figsize=(5, 5))

        plt.pie([present, absent],
                labels=["Present", "Absent"],
                colors=["green", "red"],
                autopct="%1.1f%%")

        plt.title("Attendance Analytics")
        plt.show()

    Button(button_frame,
           text="➕ Register Student",
           command=register_student,
           bg="#22c55e",
           fg="white",
           width=20).grid(row=0, column=0, padx=10)

    Button(button_frame,
           text="✔ Mark Present",
           command=mark_present,
           bg="#3b82f6",
           fg="white",
           width=20).grid(row=0, column=1, padx=10)

    Button(button_frame,
           text="❌ Mark Absent",
           command=mark_absent,
           bg="#ef4444",
           fg="white",
           width=20).grid(row=0, column=2, padx=10)

    Button(button_frame,
           text="📊 Analytics Graph",
           command=show_graph,
           bg="#8b5cf6",
           fg="white",
           width=20).grid(row=0, column=3, padx=10)

    Button(button_frame,
           text="🗑 Delete Student",
           command=delete_student,
           bg="#f97316",
           fg="white",
           width=20).grid(row=1, column=0, padx=10, pady=10)

    Button(button_frame,
           text="🧹 Clear Attendance",
           command=clear_attendance,
           bg="#eab308",
           fg="black",
           width=20).grid(row=1, column=1, padx=10, pady=10)

    Label(main_area,
          text="Registered Students",
          bg=BG,
          fg="white",
          font=("Arial", 14, "bold")).pack()

    student_table = ttk.Treeview(student_table_frame,
                                 columns=("Roll", "Name", "Class", "Section"),
                                 show="headings",
                                 height=6)

    student_table.heading("Roll", text="Roll No")
    student_table.heading("Name", text="Student Name")
    student_table.heading("Class", text="Class")
    student_table.heading("Section", text="Section")

    student_table.column("Roll", width=100)
    student_table.column("Name", width=200)
    student_table.column("Class", width=100)
    student_table.column("Section", width=100)

    student_table.pack()

    Label(main_area,
          text="Attendance Records",
          bg=BG,
          fg="white",
          font=("Arial", 14, "bold")).pack(pady=10)

    attendance_table = ttk.Treeview(attendance_table_frame,
                                    columns=("Roll", "Name", "Status", "Time"),
                                    show="headings",
                                    height=8)

    attendance_table.heading("Roll", text="Roll No")
    attendance_table.heading("Name", text="Student Name")
    attendance_table.heading("Status", text="Status")
    attendance_table.heading("Time", text="Date & Time")

    attendance_table.column("Roll", width=100)
    attendance_table.column("Name", width=200)
    attendance_table.column("Status", width=100)
    attendance_table.column("Time", width=250)

    attendance_table.pack()

    cur.execute("SELECT * FROM students")
    for row in cur.fetchall():
        student_table.insert("", "end", values=row)

    cur.execute("SELECT * FROM attendance")
    for row in cur.fetchall():
        attendance_table.insert("", "end", values=row)

    update_dashboard()

    root.mainloop()

login_window = Tk()

login_window.title("ERP Login")
login_window.geometry("350x250")
login_window.configure(bg="black")

Label(login_window,
      text="Username",
      fg="white",
      bg="black").pack(pady=5)

username_entry = Entry(login_window)
username_entry.pack()

Label(login_window,
      text="Password",
      fg="white",
      bg="black").pack(pady=5)

password_entry = Entry(login_window, show="*")
password_entry.pack()

Button(login_window,
       text="Login",
       command=login,
       bg="green",
       fg="white",
       width=15).pack(pady=15)

error_label = Label(login_window,
                    text="",
                    fg="red",
                    bg="black")

error_label.pack()

login_window.mainloop()