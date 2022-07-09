import logging
import os

from dotenv import load_dotenv
import uvicorn

from .main import app


if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(app,
                host=os.environ["HOST"],
                port=int(os.environ["PORT"]))
