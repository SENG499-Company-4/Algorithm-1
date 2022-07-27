"""Run script for REST API server

Loads environment variables from .env, sets log level and runs a Uvicorn server
serving the algorithm 1 REST API.

This was mostly set up to allow facilitate configuring Uvicorn via environment
variables.
"""

import os

from dotenv import load_dotenv
import uvicorn

from .main import app
from .. import logger


def main():
    load_dotenv()
    logger.setLevel(os.environ["LOG_LEVEL"])
    uvicorn.run(app,
                host=os.environ["HOST"],
                port=int(os.environ["PORT"]))


if __name__ == "__main__":
    main()
