"""
Curio AI — FastAPI Application Entry Point.

Wires together all routes, middleware, and exception handlers.
Run with: uvicorn app.main:app --reload
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.constants import API_PREFIX, APP_NAME, APP_VERSION
from app.config.settings import get_settings
from app.routes import chat, evaluate, report, session
from app.utils.error_handler import (
    CurioBaseError,
    curio_exception_handler,
    generic_exception_handler,
)
from app.utils.logger import get_logger

logger = get_logger(__name__)


# ── Lifespan (startup / shutdown) ────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    settings = get_settings()
    logger.info(
        "🚀 Curio AI starting up",
        extra=settings.safe_dict(),
    )
    yield
    logger.info("👋 Curio AI shutting down")


# ── Create App ───────────────────────────────────────────────────
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=(
        "Role-reversal learning API: the user teaches, "
        "the AI student challenges, evaluates, and reports."
    ),
    lifespan=lifespan,
)

# ── CORS Middleware ──────────────────────────────────────────────
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Exception Handlers ──────────────────────────────────────────
app.add_exception_handler(CurioBaseError, curio_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# ── Register Routes ─────────────────────────────────────────────
app.include_router(session.router, prefix=API_PREFIX)
app.include_router(chat.router, prefix=API_PREFIX)
app.include_router(evaluate.router, prefix=API_PREFIX)
app.include_router(report.router, prefix=API_PREFIX)


# ── Health Check ─────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check endpoint."""
    from app.services.session_manager import session_manager

    return {
        "status": "healthy",
        "app": APP_NAME,
        "version": APP_VERSION,
        "active_sessions": session_manager.active_session_count,
    }


if __name__ == "__main__":
    import uvicorn
    # This allows you to simply click "Run" in your IDE or run `python app/main.py`
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
