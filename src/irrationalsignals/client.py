"""HTTP client for the IrrationalSignals API."""

from __future__ import annotations

from typing import Optional

import requests

from .exceptions import APIError, AuthError, RateLimitError
from .models import SignalResponse


class Client:
    """Thin wrapper around GET /v1/signals.

    Usage::

        from irrationalsignals import Client

        client = Client("isk_pro_abc123...")
        response = client.get_signals()
        for signal in response.signals:
            print(signal.symbol, signal.direction, signal.win_rate)
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.irrationalsignals.com",
        timeout: float = 30,
    ):
        self._session = requests.Session()
        self._session.headers.update({
            "X-API-Key": api_key,
            "Accept": "application/json",
        })
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def get_signals(
        self,
        sector: Optional[str] = None,
        hour: Optional[int] = None,
    ) -> SignalResponse:
        """Fetch current trading signals.

        Args:
            sector: Filter by sector name (e.g. "Technology").
            hour: Same-day historical hour (10-15 ET). Max tier only.

        Returns:
            SignalResponse with parsed signals.

        Raises:
            AuthError: Invalid or missing API key (401).
            RateLimitError: Daily quota exceeded (429).
            APIError: Any other non-2xx response.
        """
        params: dict[str, str | int] = {}
        if sector is not None:
            params["sector"] = sector
        if hour is not None:
            params["hour"] = hour

        resp = self._session.get(
            f"{self._base_url}/v1/signals",
            params=params,
            timeout=self._timeout,
        )

        if resp.status_code == 401:
            detail = self._extract_detail(resp)
            raise AuthError(detail)

        if resp.status_code == 429:
            detail = self._extract_detail(resp)
            retry_after = resp.headers.get("Retry-After")
            raise RateLimitError(
                detail,
                retry_after=int(retry_after) if retry_after else None,
            )

        if not resp.ok:
            detail = self._extract_detail(resp)
            raise APIError(
                f"API request failed ({resp.status_code}): {detail}",
                status_code=resp.status_code,
                detail=detail,
            )

        return SignalResponse.from_dict(resp.json())

    @staticmethod
    def _extract_detail(resp: requests.Response) -> str:
        try:
            body = resp.json()
            return body.get("detail") or body.get("message") or str(body)
        except (ValueError, KeyError):
            return resp.text
