import logging
import uvicorn

from fastapi import FastAPI
from src.config import settings

app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",   # важно указать полный путь для Docker/IDE
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
