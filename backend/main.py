"""
FastAPI application for LexConductor external agents.

This module provides the main FastAPI application with:
- CORS middleware for cross-origin requests
- Health check endpoint
- Request/response logging middleware
- Structured JSON logging
- Routers for each agent endpoint
"""

import logging
import time
import json
from typing import Callable
from datetime import datetime

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from backend.routers import fusion, routing, memory, traceability, agent_connect

# Configure structured JSON logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

logger = logging.getLogger(__name__)


class StructuredLogger:
    """Structured JSON logger for request/response logging."""

    @staticmethod
    def log(level: str, message: str, **kwargs):
        """Log structured JSON message."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            **kwargs,
        }
        logger.info(json.dumps(log_entry))


# Create FastAPI application
app = FastAPI(
    title="LexConductor External Agents API",
    description="External agent endpoints for legal contract analysis",
    version="1.0.0",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def logging_middleware(request: Request, call_next: Callable) -> Response:
    """
    Middleware for logging all requests and responses.

    Logs:
    - Request method, path, and headers
    - Response status code and processing time
    - Any errors that occur
    """
    request_id = f"{int(time.time() * 1000)}"
    start_time = time.time()

    # Log request
    StructuredLogger.log(
        "INFO",
        "Request received",
        request_id=request_id,
        method=request.method,
        path=request.url.path,
        client_host=request.client.host if request.client else None,
    )

    try:
        # Process request
        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time

        # Log response
        StructuredLogger.log(
            "INFO",
            "Request completed",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            process_time_ms=round(process_time * 1000, 2),
        )

        # Add processing time header
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Request-ID"] = request_id

        return response

    except Exception as e:
        # Log error
        StructuredLogger.log(
            "ERROR",
            "Request failed",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            error=str(e),
            error_type=type(e).__name__,
        )

        # Return error response
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An internal error occurred",
                    "request_id": request_id,
                }
            },
        )


@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Health status and timestamp
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "lexconductor-agents",
    }


@app.get("/")
async def root():
    """
    Root endpoint with API information.

    Returns:
        dict: API information
    """
    return {
        "name": "LexConductor External Agents API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "fusion": "/fusion/analyze",
            "routing": "/routing/classify",
            "memory": "/memory/query",
            "traceability": "/traceability/generate",
        },
    }


# Include routers
app.include_router(fusion.router, prefix="/fusion", tags=["fusion"])
app.include_router(routing.router, prefix="/routing", tags=["routing"])
app.include_router(memory.router, prefix="/memory", tags=["memory"])
app.include_router(traceability.router, prefix="/traceability", tags=["traceability"])

# Include Agent Connect router (for watsonx Orchestrate integration)
app.include_router(agent_connect.router, tags=["agent-connect"])


if __name__ == "__main__":
    # Run the application
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8080, reload=True, log_level="info")
