"""Algorithm 1 API Application"""

from fastapi import FastAPI

from . import dummy
from .models import Schedule, ScheduleConstraints
from .processInput import parseInput

app = FastAPI()


@app.post('/schedule', response_model=Schedule)
def post_schedule(body: ScheduleConstraints) -> Schedule:
    """Generates a schedule"""

    parseInput(body)

    return None


@app.post("/check_schedule")
async def check_schedule():
    raise NotImplementedError()
