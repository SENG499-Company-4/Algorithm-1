from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Teacher(BaseModel):
    name: str


class CourseData(BaseModel):
    teachers: list[Teacher]


class Schedule(BaseModel):
    times: list[str]


@app.post("/", response_model=Schedule)
async def root(data: CourseData):
    print(data)

    return Schedule(["10:30", "11:30"])
