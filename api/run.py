import os

import uvicorn

from .main import app


if __name__ == "__main__":
    uvicorn.run(app,
                host=os.environ.get("HOST", "0.0.0.0"),
                port=int(os.environ.get("PORT", 8000)))
