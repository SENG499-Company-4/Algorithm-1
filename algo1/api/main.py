"""Algorithm 1 API Application"""

import logging

from fastapi import FastAPI, HTTPException, Response

from .models import Schedule, ScheduleConstraints
from .generate import generateSchedule

app = FastAPI()


@app.post('/schedule', response_model=Schedule)
def post_schedule(body: ScheduleConstraints, response: Response) -> Schedule:
    """Generates a schedule"""

    schedule, quality = generateSchedule(body)

    if schedule is None:
        raise HTTPException(status_code=400, detail="Unable to generate schedule")

    response.headers["schedule-quality"] = quality

    return schedule


@app.post("/check_schedule")
async def check_schedule():
    raise NotImplementedError()
