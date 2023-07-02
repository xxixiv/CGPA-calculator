# Code that calculates gpa

# First we import the library and modules we would use
import sqlite3
from openpyxl import Workbook
# Connect and create our Database
name = input("Please input Your name: ")
name = "_".join(name.split())  # Remove spaces and join with underscores

connection = sqlite3.connect(f"{name}.db")


# Assign the Database to a cursor for storing and retrieving of data from the database

cursor = connection.cursor()

# Create a table in our database for our data

try:
    # We use try and except to avoid error, if the table has been created already

    cursor.execute(f"""CREATE TABLE {name}( 
                    course_title text,
                    course_unit integer,
                    grade text,
                    point integer
                
                 )""")
except sqlite3.OperationalError:
    ...
# Delete the previous data from the database to avoid reoccurring figures

cursor.execute(f"DELETE FROM {name}")
# set the number of times you want the code to loop through

count = 0
ntimes = int(input("number of course offered: "))

# Using a while loop to continuously calculate the values

while count < ntimes:
    # get values from input
    course_codes = []
    course_units = []
    points = []
    grades = []
    course_title = input("Course code: ")
    course_title = course_title.upper()
    # Try for errors
    try:
        course_unit = int(input("Units: "))
    # Except errors
    except ValueError:
        print("Error!!! you inputed an alphabet. Start all over")
        quit()
    # Try for errors
    try:
        grade = input("Grade: ")
        grade = grade.upper()
    # use the if statement to calculate the points

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
    # Except Errors
    except ValueError:
        print("Incorrect Grade")
        quit()
    # increase the count by 1
    count += 1

    # insert the values gotten into the database

    cursor.execute(f"INSERT INTO {name} values ('{course_title}', '{course_unit}', '{grade}', '{point}')")

    cursor.execute(f"SELECT course_title FROM {name} WHERE course_title = '{course_title}'")
    result = cursor.fetchone()
    if result:
        course_codes.append(result[0])

    cursor.execute(f"SELECT course_unit FROM {name} WHERE course_title = '{course_title}'")
    result = cursor.fetchone()
    if result:
        course_units.append(result[0])

    cursor.execute(f"SELECT grade FROM {name} WHERE course_title = '{course_title}'")
    result = cursor.fetchone()
    if result:
        grades.append(result[0])

    cursor.execute(f"SELECT point FROM {name} WHERE course_title = '{course_title}'")
    result = cursor.fetchone()
    if result:
        points.append(result[0])

# sum the total values in point

cursor.execute(f'SELECT SUM (point) FROM {name}')

# fetch the sum total from the database

sum_point = cursor.fetchone()[0]

print(sum_point)

cursor.execute(f'SELECT SUM (course_unit) FROM {name}')

sum_unit = cursor.fetchone()[0]

print(sum_unit)

# divide the values

gpa = sum_point/sum_unit

# get all the values in the database
print(f"Dear {name}, your result is as follows..")
cursor.execute(f"SELECT * FROM {name}")
# print(cursor.fetchall())
print(course_codes)
print(course_units)
print(grades)
print(points)
print(f"Your total grade point is: {round(gpa,2)}")

# determine the class using the if statements

if 4.5 <= gpa <= 5:
    print(f"Congratulations {name}, you have a Distinction!!!")
elif gpa >= 3.5 <= 4.49:
    print(f"Congratulations {name}, You have an Upper Credit!!")
elif gpa >= 2.5 <= 3.49:
    print(f"Congratulations {name}, You have a Lower Credit!")
elif gpa >= 2.0 <= 2.49:
    print(f"Oh no, sorrow {name}!!! You have a Pass")
elif gpa >= 0 <= 1.99:
    print(f"Oh no, weep {name}!!! You Failed")
else:
    print("Your gpa cannot be calculated due to an wrong input or something try again")
# print(df)
# df.to_csv(name.csv, sep='\t')

# commit the data into the database

data = []

cursor.execute(f"SELECT course_title, course_unit, grade, point FROM {name}")
results = cursor.fetchall()

for row in results:
    data.append(row)

# Specify the path and name of the Excel file

excel_file = f"{name}_results.xlsx"

# Create a new workbook and select the active sheet

workbook = Workbook()
sheet = workbook.active

# Write the header row

sheet.append(["Course Title", "Course Unit", "Grade", "Point"])

# Write the data rows

for row in data:
    sheet.append(row)

# Save the workbook

workbook.save(excel_file)

print(f"Excel file '{excel_file}' has been created successfully!")

connection.commit()
# close database connection

connection.close()

# quit code

quit()