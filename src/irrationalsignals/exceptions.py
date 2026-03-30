"""Exception classes for the IrrationalSignals SDK."""


class APIError(Exception):
    """Base exception for API errors."""

    def __init__(self, message: str, status_code: int, detail: str = ""):
        self.status_code = status_code
        self.detail = detail
        super().__init__(message)


class AuthError(APIError):
    """Raised on 401 Unauthorized — invalid or missing API key."""

    def __init__(self, detail: str = "Invalid or missing API key"):
        super().__init__(detail, status_code=401, detail=detail)


class RateLimitError(APIError):
    """Raised on 429 Too Many Requests — daily quota exceeded."""

    def __init__(self, detail: str = "Rate limit exceeded", retry_after: int | None = None):
        self.retry_after = retry_after
        super().__init__(detail, status_code=429, detail=detail)
