from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Preference(BaseModel):
    course_num: str
    preference_num: int
    term: str


class Professor(BaseModel):
    preference_list: list[Preference]
    display_name: str
    fall_term_courses: int
    spring_term_courses: int
    summer_term_courses: int


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/", response_model=Professor)
async def root(data: Preference):
    print(data)
    return Professor(["10:30", "11:30"])
