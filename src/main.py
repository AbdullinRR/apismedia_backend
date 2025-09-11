import logging
import uvicorn

from fastapi import FastAPI

from src.api.v1.router import router as api_router


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

app = FastAPI()
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        reload=True,
    )
