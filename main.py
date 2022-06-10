from fastapi import FastAPI
from process import Process

app = FastAPI()


@app.get("/")
async def root():
    """
    Testing a get request
    """
    return {"Hello": "World"}


@app.post("/generate/")
async def generate():
    """
    Testing a post request
    """
    data = Process.process_spreadsheet()
    return data
