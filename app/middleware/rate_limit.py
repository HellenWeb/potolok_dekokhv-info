from __future__ import annotations

import time
from collections import defaultdict, deque

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, *, limit_per_minute: int) -> None:
        super().__init__(app)
        self.limit_per_minute = limit_per_minute
        self.requests: dict[str, deque[float]] = defaultdict(deque)
        self.window_seconds = 60.0

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS" or self.limit_per_minute <= 0:
            return await call_next(request)

        forwarded_for = request.headers.get("x-forwarded-for", "")
        client_host = forwarded_for.split(",")[0].strip() if forwarded_for else None
        identifier = client_host or (request.client.host if request.client else "anonymous")

        now = time.monotonic()
        bucket = self.requests[identifier]

        while bucket and now - bucket[0] > self.window_seconds:
            bucket.popleft()

        if len(bucket) >= self.limit_per_minute:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Too many requests", "error_code": "rate_limit_exceeded"},
            )

        bucket.append(now)
        return await call_next(request)
