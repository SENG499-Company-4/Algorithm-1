from fastapi import FastAPI

from process import Process
from models import Schedule

app = FastAPI()


@app.post("/generate_schedule", response_model=Schedule)
async def generate_schedule(schedule: Schedule):
    """Generates a schedule"""

    # data = Process.process_spreadsheet()

    return Schedule(fallTermCourses=[],
                    springTermCourses=[],
                    summerTermCourses=[])


@app.post("/check_schedule")
async def check_schedule():
    raise NotImplementedError()
