import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import async_session
from app.core.logger import get_logger

logger = get_logger("app")


async def _periodic_health_check():
    interval = settings.HEALTH_CHECK_INTERVAL_SECONDS
    logger.info("Background health check started (every %ds)", interval)
    while True:
        await asyncio.sleep(interval)
        try:
            async with async_session() as session:
                await session.execute(text("SELECT 1"))
            logger.info("Background health check: OK")
        except Exception as exc:
            logger.error("Background health check FAILED: %s", exc)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Thermodyne CRM API started (env=%s)", settings.ENVIRONMENT)
    task = asyncio.create_task(_periodic_health_check())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
    logger.info("Thermodyne CRM API shutting down")


docs_kwargs = {}
if settings.is_production:
    docs_kwargs = {"docs_url": None, "redoc_url": None, "openapi_url": None}

app = FastAPI(
    title="Thermodyne CRM API",
    version="0.1.0",
    lifespan=lifespan,
    **docs_kwargs,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("%s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("%s %s -> %s", request.method, request.url.path, response.status_code)
    return response
