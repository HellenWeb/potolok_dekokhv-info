#!/usr/bin/env python3

"""

    date: 23.07.2026

    Файл для безопасного подключения к API и его работы

"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp
import time
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            # Можно делать per-endpoint, но глобально:
            await limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")(call_next)(request)
            response = await call_next(request)
            return response
        except RateLimitExceeded as e:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"}
            )

# Security Headers Middleware
async def add_security_headers(app: ASGIApp):
    async def middleware(request: Request, call_next):
        response: Response = await call_next(request)
        
        # Основные заголовки безопасности
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        # CSP (Content Security Policy) — очень важно!
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )
        return response
    return middleware