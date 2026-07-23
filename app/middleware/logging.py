#!/usr/bin/env python3

"""

    date: 23.07.2026

    Файл для подробного логирования

"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        res = await call_next(request)
        process_time = time.time() - start_time
        logging.info(
            f"{request.method} {request.url.path}"
            f"completed in {process_time:.4f} with status {res.status_code}"
        )
        return res