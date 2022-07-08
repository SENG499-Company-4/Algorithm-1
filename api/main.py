"""Algorithm 1 API Application"""

from email.quoprimime import body_check
from fastapi import FastAPI

from . import dummy
from .models import Schedule, ScheduleConstraints
from .generate import generateSchedule

app = FastAPI()


@app.post('/schedule', response_model=Schedule)
def post_schedule(body: ScheduleConstraints) -> Schedule:
    """Generates a schedule"""

    return generateSchedule(body)


@app.post("/check_schedule")
async def check_schedule():
    raise NotImplementedError()
