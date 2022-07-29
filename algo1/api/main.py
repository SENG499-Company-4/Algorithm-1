"""Algorithm 1 API Application"""

from fastapi import FastAPI, HTTPException

from .models import Schedule, ScheduleConstraints
from .generate import generate_schedule

app = FastAPI()


@app.post("/schedule", response_model=Schedule)
def post_schedule(body: ScheduleConstraints) -> Schedule:
    """Endpoint for accepting schedule generation requests"""

    schedule = generate_schedule(body)

    if schedule is None:
        raise HTTPException(status_code=400,
                            detail="Unable to generate schedule")

    return schedule


@app.post("/check_schedule")
async def check_schedule():
    raise NotImplementedError()
