import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from openpyxl import Workbook

def set_entries():
    global ntimes, course_entries, unit_entries, grade_entries

    try:
        ntimes = int(ntimes_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid number of courses entered.")
        return

    for i in range(ntimes):
        course_label = tk.Label(scrollable_frame, text=f"Course {i + 1}:")
        course_label.pack()

        course_entry = tk.Entry(scrollable_frame)
        course_entry.pack()
        course_entries.append(course_entry)

        unit_label = tk.Label(scrollable_frame, text="Units:")
        unit_label.pack()

        unit_entry = tk.Entry(scrollable_frame)
        unit_entry.pack()
        unit_entries.append(unit_entry)

        grade_label = tk.Label(scrollable_frame, text="Grade:")
        grade_label.pack()

        grade_entry = tk.Entry(scrollable_frame)
        grade_entry.pack()
        grade_entries.append(grade_entry)

def save_results():
    name = name_entry.get()
    if not name:
        messagebox.showerror("Error", "Please enter your name.")
        return

    # Connect to the database
    connection = sqlite3.connect(f"{name}.db")
    name = "_".join(name.split())  # Remove spaces and join with underscores
    cursor = connection.cursor()

    # Create the table if it doesn't exist
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {name} (
                    course_title TEXT,
                    course_unit INTEGER,
                    grade TEXT,
                    point INTEGER
                    )""")

    # Delete previous data from the table
    cursor.execute(f"DELETE FROM {name}")

    # Save the course data to the database
    try:
        for i in range(ntimes):
            course_title = course_entries[i].get().upper()
            course_unit = int(unit_entries[i].get())
            grade = grade_entries[i].get().upper()

            if grade not in {"A", "B", "C", "D", "E", "F"}:
                messagebox.showerror("Error", "Incorrect grade entered.")
                return

            if grade == "A":
                point = 5 * course_unit
            elif grade == "B":
                point = 4 * course_unit
            elif grade == "C":
                point = 3 * course_unit
            elif grade == "D":
                point = 2 * course_unit
            elif grade == "E":
                point = 1 * course_unit
            elif grade == "F":
                point = 0 * course_unit

            cursor.execute(f"INSERT INTO {name} VALUES (?, ?, ?, ?)",
                           (course_title, course_unit, grade, point))
    except ValueError:
        messagebox.showerror("Error", "Invalid course unit entered.")
        return

    # Calculate gpa
    cursor.execute(f'SELECT SUM(point) FROM {name}')
    sum_point = cursor.fetchone()[0]

    cursor.execute(f'SELECT SUM(course_unit) FROM {name}')
    sum_unit = cursor.fetchone()[0]

    gpa = sum_point / sum_unit

    # Get all the values from the database
    cursor.execute(f"SELECT * FROM {name}")
    results = cursor.fetchall()

    # Save results to Excel file
    excel_file = f"{name}_results.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["Course Title", "Course Unit", "Grade", "Point"])

    for row in results:
        sheet.append(row)

    workbook.save(excel_file)

    # Display gpa and class
    messagebox.showinfo("Result", f"gpa: {round(gpa, 2)}")

    if 4.5 <= gpa <= 5:
        messagebox.showinfo("Result", f"Congratulations {name}, you have a Distinction!")
    elif 3.5 <= gpa < 4.5:
        messagebox.showinfo("Result", f"Congratulations {name}, you have an Upper Credit!")
    elif 2.5 <= gpa < 3.5:
        messagebox.showinfo("Result", f"Congratulations {name}, you have a Lower Credit!")
    elif 2.0 <= gpa < 2.5:
        messagebox.showinfo("Result", f"Oh no, {name}, you have a Pass!")
    elif 0 <= gpa < 2.0:
        messagebox.showinfo("Result", f"Oh no, {name}, you Failed!")
    else:
        messagebox.showinfo("Result", "Your gpa cannot be calculated.")

    # Commit and close the database connection
    connection.commit()
    connection.close()


def clear_entries():
    name_entry.delete(0, tk.END)
    ntimes_entry.delete(0, tk.END)

    for entry in course_entries:
        entry.destroy()
    for entry in unit_entries:
        entry.destroy()
    for entry in grade_entries:
        entry.destroy()

def show_course_details():
    details = ""
    for i in range(ntimes):
        course_title = course_entries[i].get()
        course_unit = unit_entries[i].get()
        grade = grade_entries[i].get()
        details += f"Course {i + 1}:\nTitle: {course_title}\nUnits: {course_unit}\nGrade: {grade}\n\n"

    messagebox.showinfo("Course Details", details)

# Create the Tkinter window
window = tk.Tk()

# Set the window title
window.title("Gpa Calculator")

# Set the window icon
window.iconbitmap("icon.ico")

# Create a scrollable frame
canvas = tk.Canvas(window)
scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Create the GUI elements
name_label = tk.Label(scrollable_frame, text="Name:")
name_label.pack(anchor="center")
name_entry = tk.Entry(scrollable_frame)
name_entry.pack(anchor="center", pady=5)

ntimes_label = tk.Label(scrollable_frame, text="Number of Courses Offered:")
ntimes_label.pack(anchor="center")
ntimes_entry = tk.Entry(scrollable_frame)
ntimes_entry.pack(anchor="center", pady=5)

course_entries = []
unit_entries = []
grade_entries = []

set_entries_button = ttk.Button(scrollable_frame, text="Set Entries", command=set_entries)
set_entries_button.pack(anchor="center", pady=10)

calculate_button = ttk.Button(scrollable_frame, text="Calculate", command=save_results)
calculate_button.pack(anchor="center", pady=5)

show_details_button = ttk.Button(scrollable_frame, text="Show Course Details", command=show_course_details)
show_details_button.pack(anchor="center", pady=5)

clear_button = ttk.Button(scrollable_frame, text="Clear Entries", command=clear_entries)
clear_button.pack(anchor="center", pady=5)

# Start the Tkinter event loop
window.mainloop()
