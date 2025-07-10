from fastapi import FastAPI

from .dispatcher import router

app = FastAPI()
app.include_router(router)

__all__ = ["app"]
