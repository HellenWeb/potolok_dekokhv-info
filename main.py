from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from app.api.router import api_router
from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.db.init_db import init_db
from app.middleware.logging import LoggingMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.security import SecurityHeadersMiddleware


settings = get_settings()

@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield

def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="2.0.0",
        lifespan=lifespan,
    )

    if settings.is_production:
        app.add_middleware(HTTPSRedirectMiddleware)

    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(RateLimitMiddleware, limit_per_minute=settings.security.rate_limit_per_minute)

    if "*" not in settings.security.allowed_hosts:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.security.allowed_hosts,
        )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.security.cors_origins,
        allow_origin_regex=settings.security.cors_origin_regex,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", settings.telegram.init_data_header, "X-Debug-Telegram-Id"],
        expose_headers=["Content-Type"],
    )

    register_exception_handlers(app)
    app.include_router(api_router)

    @app.get("/", tags=["Health"])
    async def root() -> dict[str, str]:
        return {
            "project": settings.PROJECT_NAME,
            "status": "ok",
            "version": "2.0.0",
        }

    return app


app = create_application()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        proxy_headers=True,
        forwarded_allow_ips="*",
        reload=settings.DEBUG,
    )
