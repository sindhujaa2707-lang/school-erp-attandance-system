from tkinter import *

students = []

def present():
    name = entry.get()
    students.append(name + " - Present")
    result.config(text="\n".join(students))
    entry.delete(0, END)
    update_count()

def absent():
    name = entry.get()
    students.append(name + " - Absent")
    result.config(text="\n".join(students))
    entry.delete(0, END)
    update_count()

root = Tk()
root.title("Smart Attendance System")
root.geometry("500x400")

label = Label(root, text="Enter Student Name", font=("Arial", 14))
label.pack()

entry = Entry(root)
entry.pack()

present_button = Button(root, text="Present", command=present, bg="green", fg="white")
present_button.pack()

absent_button = Button(root, text="Absent", command=absent, bg="red", fg="white")
absent_button.pack()

def clear_all():
    students.clear()
    result.config(text="")

def update_count():
    count_label.config(text="Total Records: " + str(len(students)))

def save_data():
    print("Saving data...")

    file_path = "C:\\Users\\Lenovo\\attendance.txt"

    with open(file_path, "w") as f:
        for item in students:
            f.write(item + "\n")

    print("Saved at:", file_path)

clear_button = Button(root, text="Clear All", command=clear_all, bg="blue", fg="white")
clear_button.pack()

save_button = Button(root, text="Save Data", command=save_data, bg="purple", fg="white")
save_button.pack()

result = Label(root, text="")
result.pack()

count_label = Label(root, text="Total Records: 0")
count_label.pack()

root.mainloop()