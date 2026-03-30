"""IrrationalSignals Python SDK — thin wrapper around the signals API."""

from .client import Client
from .exceptions import APIError, AuthError, RateLimitError
from .models import ExecutionGuidance, PreflightData, Signal, SignalResponse

__all__ = [
    "Client",
    "APIError",
    "AuthError",
    "RateLimitError",
    "ExecutionGuidance",
    "PreflightData",
    "Signal",
    "SignalResponse",
]
