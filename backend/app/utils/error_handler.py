"""
Curio AI — Error Handling: Custom Exceptions + FastAPI Exception Handlers.

Custom exceptions are raised by services. The FastAPI handlers registered
in main.py catch them and return a consistent error envelope:

    {
        "success": false,
        "error": {
            "code": "NOT_FOUND",
            "message": "Session xyz not found",
            "details": null
        },
        "request_id": "req-abc123"
    }
"""

from typing import Any, Optional

from fastapi import Request
from fastapi.responses import JSONResponse


# ═══════════════════════════════════════════════════════════════════
#  Custom Exceptions
# ═══════════════════════════════════════════════════════════════════

class CurioBaseError(Exception):
    """Base exception for all Curio errors."""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: Optional[Any] = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class CurioValidationError(CurioBaseError):
    """Raised when input validation fails."""

    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=422,
            details=details,
        )


class NotFoundError(CurioBaseError):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found", details: Optional[Any] = None):
        super().__init__(
            message=message,
            code="NOT_FOUND",
            status_code=404,
            details=details,
        )


class SessionExpiredError(CurioBaseError):
    """Raised when a session has expired past its TTL."""

    def __init__(self, session_id: str):
        super().__init__(
            message=f"Session '{session_id}' has expired",
            code="SESSION_EXPIRED",
            status_code=410,
            details={"session_id": session_id},
        )


class AIProviderError(CurioBaseError):
    """Raised when the AI provider fails or returns unexpected output."""

    def __init__(self, message: str = "AI provider error", details: Optional[Any] = None):
        super().__init__(
            message=message,
            code="AI_PROVIDER_ERROR",
            status_code=502,
            details=details,
        )


# ═══════════════════════════════════════════════════════════════════
#  Error Response Builder
# ═══════════════════════════════════════════════════════════════════

def _build_error_response(
    status_code: int,
    code: str,
    message: str,
    details: Optional[Any] = None,
    request_id: Optional[str] = None,
) -> JSONResponse:
    """Build a consistent JSON error response."""
    body = {
        "success": False,
        "data": None,
        "error": {
            "code": code,
            "message": message,
        },
    }
    if details is not None:
        body["error"]["details"] = details
    if request_id:
        body["request_id"] = request_id
    return JSONResponse(status_code=status_code, content=body)


# ═══════════════════════════════════════════════════════════════════
#  FastAPI Exception Handlers
# ═══════════════════════════════════════════════════════════════════

async def curio_exception_handler(request: Request, exc: CurioBaseError) -> JSONResponse:
    """Handle all CurioBaseError subtypes."""
    request_id = request.headers.get("X-Request-ID") or getattr(request.state, "request_id", None)
    return _build_error_response(
        status_code=exc.status_code,
        code=exc.code,
        message=exc.message,
        details=exc.details,
        request_id=request_id,
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all for unhandled exceptions."""
    request_id = request.headers.get("X-Request-ID") or getattr(request.state, "request_id", None)
    return _build_error_response(
        status_code=500,
        code="INTERNAL_ERROR",
        message="An unexpected error occurred",
        details=str(exc) if request.app.debug else None,
        request_id=request_id,
    )
