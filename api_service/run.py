import os
import sys

import uvicorn
from fastapi import FastAPI
from api_service.Getters.healthcheck import router as healthcheck_router
from api_service.logs import create_logger
import logging

LOGGER = create_logger(__name__)


def app():
    """
    Application factory
    :return:
    """
    LOGGER.info("Starting FastAPI")
    fast_api_app = FastAPI()
    fast_api_app.include_router(healthcheck_router)
    return fast_api_app


def main():
    """Run fastapi service"""
    uvicorn.run(
        "run:app",
        host="0.0.0.0",
        port=int(os.getenv("FAST_API_PORT", "8000")),
        reload=True,
    )


if __name__ == "__main__":
    main()