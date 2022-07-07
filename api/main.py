"""Algorithm 1 API Application"""

from .parse_input import (
    courses_to_schedule,
    fall_courses,
    fall_term_courses_to_pref_matrix,
    spring_courses,
    spring_term_courses_to_pref_matrix,
    summer_courses,
    summer_term_courses_to_pref_matrix,
)
from fastapi import FastAPI

from . import dummy
from .models import Input, Schedule

app = FastAPI()


@app.post("/schedule", response_model=Schedule)
async def generate_schedule(input: Input):
    """Generates a schedule"""

    return dummy.rand_schedule()


@app.post("/check_schedule")
async def check_schedule():
    raise NotImplementedError()


@app.get("/schedule", response_model=Schedule)
async def generate_schedule(input: Input):
    courses_to_schedule = courses_to_schedule(input)
    fall_courses = fall_term_courses_to_pref_matrix(courses_to_schedule)
    spring_courses = spring_term_courses_to_pref_matrix(courses_to_schedule)
    summer_courses = summer_term_courses_to_pref_matrix(courses_to_schedule)
    return Schedule(
        fallTermCourses=fall_courses,
        springTermCourses=spring_courses,
        summerTermCoures=summer_courses,
    )
