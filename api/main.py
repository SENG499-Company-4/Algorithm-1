"""Algorithm 1 API Application"""

from .parse_input import (
    courses_to_schedule,
    fall_courses,
    spring_courses,
    summer_courses,
)
from fastapi import FastAPI

from . import dummy
from .models import Input, Schedule

app = FastAPI()


@app.post("/schedule", response_model=Schedule)
async def generate_schedule():
    """Generates a schedule"""

    return dummy.rand_schedule()


@app.post("/check_schedule")
async def check_schedule():
    raise NotImplementedError()


@app.get("/schedule") #response_model=Schedule)
async def generate_schedule(input: Input):
    courses_to_schedule_ = courses_to_schedule(input)
    fall_courses_ = fall_courses(courses_to_schedule_)
    spring_courses_ = spring_courses(courses_to_schedule_)
    summer_courses_ = summer_courses(courses_to_schedule_)
    '''
    return Schedule(
        fallTermCourses=fall_courses,
        springTermCourses=spring_courses,
        summerTermCoures=summer_courses,
    )
    '''
    return fall_courses_
