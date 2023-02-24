# Code that calculates CGPA

# First we import the library and modules we would use
import sqlite3
# Connect and create our Database

connection = sqlite3.connect("CGPA Calculator")

# Assign the Database to a cursor for storing and retrieving of data from the database

cursor = connection.cursor()

# Create a table in our database for our data
name = input("Please input Your name: ")
try:
    # We use try and except to avoid error, if the table has been created already

    cursor.execute("""CREATE TABLE cgpa( 
                    course_title text,
                    course_unit integer,
                    grade text,
                    point integer
                
                 )""")
except sqlite3.OperationalError:
    ...
# Delete the previous data from the database to avoid reoccurring figures

cursor.execute(f"DELETE FROM cgpa")
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

    cursor.execute(f"INSERT INTO cgpa values ('{course_title}', '{course_unit}', '{grade}', '{point}')")

    course_codes = [cursor.execute(f"SELECT [0] FROM {name} value {course_title}")].append
    course_units =[cursor.execute(f"SELECT [0] FROM {name} value {course_unit}")].append
    grades = [cursor.execute(f"SELECT [0] FROM {name} value {grade}")].append
    point = [cursor.execute(f"SELECT [0] FROM {name} value {point}")].append


# sum the total values in point

cursor.execute(f'SELECT SUM (point) FROM cgpa')

# fetch the sum total from the database

sum_point = cursor.fetchone()[0]

print(sum_point)

cursor.execute(f'SELECT SUM (course_unit) FROM cgpa')

sum_unit = cursor.fetchone()[0]

print(sum_unit)

# divide the values

cgpa = sum_point/sum_unit

# get all the values in the database
print(f"Dear {name}, your result is as follows..")
cursor.execute(f"SELECT * FROM cgpa")
# print(cursor.fetchall())
print(course_codes)
print(course_units)
print(grades)
print(points)
print(f"Your total grade point is: {round(cgpa,2)}")

# determine the class using the if statements

if cgpa >= 4.5 <= 5:
    print(f"Congratulations {name}, you have a Distinction!!!")
elif cgpa >= 3.5 <= 4.49:
    print(f"Congratulations {name}, You have an Upper Credit!!")
elif cgpa >= 2.5 <= 3.49:
    print(f"Congratulations {name}, You have a Lower Credit!")
elif cgpa >= 2.0 <= 2.49:
    print(f"Oh no, sorrow {name}!!! You have a Pass")
elif cgpa >= 0 <= 1.99:
    print(f"Oh no, weep {name}!!! You Failed")
else:
    print("Your CGPA cannot be calculated due to an wrong input or something try again")
# print(df)
# df.to_csv(name.csv, sep='\t')

# commit the data into the database

connection.commit()
# close database connection

connection.close()

# quit code

quit()