from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Preference(BaseModel):
    course_num: str      # ex. CSC 226
    preference_num: int  # ex. 6
    term: str            # ex. fall


class Professor(BaseModel):
    preference_list: list[Preference]
    display_name: str          # ex. Michael Zastre
    fall_term_courses: int     # ex. 2
    spring_term_courses: int   # ex. 1
    summer_term_courses: int   # ex. 0


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/", response_model=Professor)
async def root(data: Preference):
    print(data)
    return Professor(["10:30", "11:30"])


