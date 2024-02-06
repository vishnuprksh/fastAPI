from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import Optional
import random

#creating the app object
app = FastAPI()

students = {
    1: {
        "name" : "john",
        "age": 17,
        "year": "year 12"
    },
    2: {
        "name" : "sasi",
        "age": 18,
        "year": "year 13"
    }
}

class Student(BaseModel):
    name : str
    age: int
    year: str

class UpdateStudent(BaseModel):
    name : Optional[str] = None
    age : Optional[int] = None
    year : Optional[str] = None


@app.get("/")
def index():
    return {"name": "hello fastapi", "data": 999}

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(description="The student id you want to view", gt=0)):
    return students[student_id]

@app.get("/get-by-name")
def get_student(name: str = None):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not found"}

@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "student exists"}
    students[student_id] = student
    return students[student_id]

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "student details not found"}
    if student.name is not None:
        students[student_id]["name"] = student.name
    if student.age is not None:
        students[student_id]["age"] = student.age
    if student.year is not None:
        students[student_id]["year"] = student.year
    return students[student_id]

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "student does not exists"}
    del students[student_id]
    return {"Message": "Student deleted successfully"}


@app.get("/random/{limit}")
async def get_random(limit: int):
    rn: int = random.randint(0, limit)
    return {"number": rn, "limit": limit}