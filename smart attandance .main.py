from tkinter import *
from tkinter import ttk
from datetime import datetime
import sqlite3
import matplotlib.pyplot as plt
import os

if os.path.exists("attendance.db"):
    pass

conn = sqlite3.connect("attendance.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS attendance (
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

    global root, entry, table

    root = Tk()
    root.title("School ERP Attendance System")
    root.geometry("900x600")
    root.configure(bg="#0f172a")

    SIDEBAR = "#111827"
    BG = "#0f172a"
    CARD = "#1f2937"

    sidebar = Frame(root, bg=SIDEBAR, width=200)
    sidebar.pack(side=LEFT, fill=Y)

    main_area = Frame(root, bg=BG)
    main_area.pack(side=LEFT, fill=BOTH, expand=True)

    Label(sidebar,
          text="🏫 SCHOOL ERP",
          fg="white",
          bg=SIDEBAR,
          font=("Arial", 14, "bold")).pack(pady=20)

    Label(main_area,
          text="Attendance Dashboard",
          font=("Arial", 18, "bold"),
          fg="white",
          bg=BG).pack(pady=10)

    card_frame = Frame(main_area, bg=BG)
    card_frame.pack(pady=10)

    total_label = Label(card_frame, text="📌 Total: 0",
                        bg=CARD, fg="white",
                        width=18, pady=15)

    present_label = Label(card_frame, text="🟢 Present: 0",
                          bg=CARD, fg="white",
                          width=18, pady=15)

    absent_label = Label(card_frame, text="🔴 Absent: 0",
                         bg=CARD, fg="white",
                         width=18, pady=15)

    total_label.pack(side=LEFT, padx=10)
    present_label.pack(side=LEFT, padx=10)
    absent_label.pack(side=LEFT, padx=10)

    input_frame = Frame(main_area, bg=BG)
    input_frame.pack(pady=10)

    entry = Entry(input_frame, font=("Arial", 14), width=30)
    entry.pack()

    button_frame = Frame(main_area, bg=BG)
    button_frame.pack(pady=10)

    table_frame = Frame(main_area)
    table_frame.pack(pady=10)

    def update_dashboard():
        cur.execute("SELECT COUNT(*) FROM attendance")
        total = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM attendance WHERE status='Present'")
        present = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM attendance WHERE status='Absent'")
        absent = cur.fetchone()[0]

        total_label.config(text=f"📌 Total: {total}")
        present_label.config(text=f"🟢 Present: {present}")
        absent_label.config(text=f"🔴 Absent: {absent}")

    def present():
        name = entry.get()
        if name == "":
            return
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cur.execute("INSERT INTO attendance VALUES (?, ?, ?)",
                    (name, "Present", time))
        conn.commit()

        table.insert("", "end", values=(name, "Present", time))
        entry.delete(0, END)

        update_dashboard()

    def absent():
        name = entry.get()
        if name == "":
            return
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cur.execute("INSERT INTO attendance VALUES (?, ?, ?)",
                    (name, "Absent", time))
        conn.commit()

        table.insert("", "end", values=(name, "Absent", time))
        entry.delete(0, END)

        update_dashboard()

    def delete_selected():
        for item in table.selection():
            values = table.item(item)["values"]
            cur.execute("DELETE FROM attendance WHERE name=? AND time=?", (values[0], values[2]))
            conn.commit()
            table.delete(item)

        update_dashboard()

    def clear_all():
        cur.execute("DELETE FROM attendance")
        conn.commit()

        for item in table.get_children():
            table.delete(item)

        update_dashboard()

    def search_student():
        name = entry.get().lower()
        for row in table.get_children():
            values = table.item(row)['values']
            if name in str(values[0]).lower():
                table.selection_set(row)
                table.see(row)
                return

    def show_graph():
        cur.execute("SELECT COUNT(*) FROM attendance WHERE status='Present'")
        present = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM attendance WHERE status='Absent'")
        absent = cur.fetchone()[0]

        plt.figure()
        plt.pie([present, absent],
                labels=["Present", "Absent"],
                colors=["green", "red"],
                autopct="%1.1f%%")
        plt.title("Attendance Report")
        plt.show()

    Button(button_frame, text="✔ Present",
           command=present,
           bg="#22c55e", fg="white",
           width=15).grid(row=0, column=0, padx=5)

    Button(button_frame, text="❌ Absent",
           command=absent,
           bg="#ef4444", fg="white",
           width=15).grid(row=0, column=1, padx=5)

    Button(button_frame, text="🔍 Search",
           command=search_student,
           bg="#3b82f6", fg="white",
           width=15).grid(row=0, column=2, padx=5)

    Button(button_frame, text="📊 Graph",
           command=show_graph,
           bg="#8b5cf6", fg="white",
           width=15).grid(row=1, column=0, padx=5, pady=5)

    Button(button_frame, text="🧹 Clear All",
           command=clear_all,
           bg="#f59e0b", fg="black",
           width=15).grid(row=1, column=1, padx=5, pady=5)

    Button(button_frame, text="🗑 Delete",
           command=delete_selected,
           bg="#fb923c", fg="white",
           width=15).grid(row=1, column=2, padx=5, pady=5)

    table = ttk.Treeview(table_frame,
                         columns=("Name", "Status", "Time"),
                         show="headings",
                         height=12)

    table.heading("Name", text="Student Name")
    table.heading("Status", text="Status")
    table.heading("Time", text="Date & Time")

    table.column("Name", width=200)
    table.column("Status", width=100)
    table.column("Time", width=250)

    table.pack()

    cur.execute("SELECT * FROM attendance")
    for row in cur.fetchall():
        table.insert("", "end", values=row)

    update_dashboard()

    root.mainloop()

login_window = Tk()
login_window.title("Login")
login_window.geometry("350x250")
login_window.configure(bg="black")

Label(login_window, text="Username", bg="black", fg="white").pack()
username_entry = Entry(login_window)
username_entry.pack()

Label(login_window, text="Password", bg="black", fg="white").pack()
password_entry = Entry(login_window, show="*")
password_entry.pack()

Button(login_window, text="Login",
       command=login,
       bg="green", fg="white").pack(pady=10)

error_label = Label(login_window, text="", fg="red", bg="black")
error_label.pack()

login_window.mainloop()