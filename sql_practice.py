import sqlite3

conn=sqlite3.connect(":memory:")

cur=conn.cursor()

cur.execute("CREATE table Students(id INTEGER,name TEXT,city TEXT,course TEXT,score INTEGER)")
cur.executemany("INSERT INTO students VALUES (?,?,?,?,?)", [
    (1, "Asha",  "Chennai", "Python", 85),
    (2, "Ravi",  "Madurai", "Python", 62),
    (3, "Priya", "Chennai", "SQL",    91),
    (4, "Karan", "Trichy",  "SQL",    74),
    (5, "Meena", "Madurai", "Python", 55),
    (6, "Sam",   "Trichy",  "React",  88),
    (7, "Divya", "Chennai", "React",  67),
])


def run (query):
    print(query)
    for row in cur.execute(query):
        print(" ",row)
    print()

run("SELECT * FROM Students")
run("SELECT city FROM Students")

run("SELECT * FROM Students WHERE city ='Chennai'")
run("Select name from Students where score > 80")
run ("select name from Students where course='SQL' or course='Python'")


run("select count(*) from Students")
run("select avg(score) from students")
run("select max(score) from students")
run("select min(score) from students")
run("select sum(score) from students")


run("select course ,count(*) from students Group by course")
run("select city,count(*) from students group by city")
run("select city,avg(score) from students group by city")


run("select city,count(*) from students where score >60 group by city")
run("select course,count(*) from students where score >60 group by course")

# Number of students in each city.
run("select city, count(*) from students group by city")
# Number of students with a score above 70 in each course.

run("select course,count(*) from students where score > 70 group by course")