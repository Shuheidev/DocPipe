import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .dispatcher import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(router)


@app.exception_handler(Exception)
async def handle_exception(request: Request, exc: Exception) -> JSONResponse:
    """Return JSON errors and log technical details."""
    logger.exception("Unhandled error")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "details": str(exc)},
    )

__all__ = ["app"]
