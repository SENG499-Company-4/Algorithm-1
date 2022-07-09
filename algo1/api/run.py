import os

from dotenv import load_dotenv
import uvicorn

from .main import app
from .. import logger


if __name__ == "__main__":
    load_dotenv()
    logger.setLevel(os.environ["LOG_LEVEL"])
    uvicorn.run(app,
                host=os.environ["HOST"],
                port=int(os.environ["PORT"]))
