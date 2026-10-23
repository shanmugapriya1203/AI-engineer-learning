import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()

cur.execute("CREATE TABLE students (id INTEGER, name TEXT, city TEXT)")
cur.execute("CREATE TABLE results (student_id INTEGER, course TEXT, score INTEGER)")
cur.execute("CREATE TABLE courses (course TEXT, trainer TEXT, fee INTEGER)")

cur.executemany("INSERT INTO students VALUES (?,?,?)", [
    (1, "Asha", "Chennai"), (2, "Ravi", "Madurai"), (3, "Priya", "Chennai"),
    (4, "Karan", "Trichy"), (5, "Meena", "Madurai"), (6, "Sam", "Trichy"),
])
cur.executemany("INSERT INTO results VALUES (?,?,?)", [
    (1, "Python", 85), (1, "SQL", 78), (2, "Python", 62), (3, "SQL", 91),
    (3, "React", 80), (4, "SQL", 74), (6, "React", 88), (6, "Python", 70),
])
cur.executemany("INSERT INTO courses VALUES (?,?,?)", [
    ("Python", "Arun", 5000), ("SQL", "Bala", 4000), ("React", "Chitra", 6000),
])

def run(query):
    print(query)
    for row in cur.execute(query):
        print("  ", row)
    print()

# ---- write your queries below this line ----
run("SELECT COUNT(*) FROM students")
run("SELECT COUNT(*) FROM results")

# Level 1: Basic joins (students + results)
# Name, course and score for every result.
# Name, course and score where the score is 80 or more.
# Name and course for students from Chennai.
# Names of students who took Python.
# Name, course and score, sorted by score, highest first.
# The top 3 scores with the student's name and course.


run("select students.name,results.course,results.score from students join results on students.id=results.student_id")
run("select students.name,results.course,results.score from students join results on students.id=results.student_id where score>=80")
run("select students.name,results.course from students join  results on students.id= results.student_id where city='Chennai' ")
run ("select students.name,results.course from students join results on students.id=results.student_id where course='Python'")
run("select students.name,results.course,results.score from students join results on students.id=results.student_id order by results.score desc")
run("select students.name,results.course,results.score from students join results on students.id=results.student_id order by results.score desc limit 3")

# Level 2: Join + GROUP BY
# The number of courses each student took.
# The average score of each student.
# The average score for each city.
# The total score for each city.
# How many different students from each city have results? (Hint: COUNT(DISTINCT ...).)
# Stretch: students whose average score is above 80. (Hint: HAVING.)


run("select students.name ,count(results.course) as coursecount from students join results on students.id=results.student_id group by students.id,students.name")
run("select students.name,avg(results.score) from students join results on students.id=results.student_id group by students.name")
run("select students.city, avg(results.score) from students join results on students.id=results.student_id group by students.city")
run("select students.city, sum(results.score) from students join results on students.id=results.student_id group by students.city")
run("select students.city, sum(results.score) from students join results on students.id=results.student_id group by students.city")
run("select students.city,count(distinct students.id) from students join results on students.id= results.student_id group by students.city")
run("select students.name,avg(results.score)from students join results on students.id=results.student_id group by students.name having avg(results.score)>80 ")


# Student name, course and trainer for every result.
# Names of students taught by Bala.
# The total fee for each student (the sum of the fees of the courses they took).
# The average score for each trainer