from fastapi import FastAPI

from . import dummy
from .models import Input, Schedule

app = FastAPI()


@app.post("/schedule", response_model=Schedule)
async def generate_schedule(input: Input):
    """Generates a schedule"""

    # data = Process.process_spreadsheet()

    return Schedule(fallTermCourses=[],
                    springTermCourses=[],
                    summerTermCourses=[])


@app.post("/check_schedule")
async def check_schedule():
    raise NotImplementedError()
