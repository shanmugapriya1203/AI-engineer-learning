from pydantic import BaseModel, Field, ValidationError, EmailStr

class Student(BaseModel):
    name: str
    age: int = Field(ge=15, le=60)
    skills: list[str] = []
    email: EmailStr

# test 1: valid
s = Student(name="Asha", age=24, skills=["python", "sql"], email="asha@gmail.com")
print(s.model_dump())

# test 2: invalid email (no @)
try:
    Student(name="Ravi", age=24, email="sam1203gmail.com")
except ValidationError as e:
    print("Email error:\n", e)

# test 3: invalid age (below 15)
try:
    Student(name="Ravi", age=13, email="ravi@gmail.com")
except ValidationError as e:
    print("Age error:\n", e)