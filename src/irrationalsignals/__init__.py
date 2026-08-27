"""IrrationalSignals Python SDK — thin wrapper around the signals API.

DEPRECATED: IrrationalSignals was wound down in May 2026 and the API is offline.
This package is no longer maintained and will not function against a live
service. It remains published for reference only.
"""

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
