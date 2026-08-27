"""Dataclass models matching the IrrationalSignals API response."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class ExecutionGuidance:
    """Entry/exit targets and risk levels for a signal."""

    entry_price: float
    expected_return_pct: float
    """Expected return from entry to exit target, as a decimal (0.008 = 0.8%).

    Derived from the signal type's historical forward-return distribution:
    average 2.5-hour (150-minute) forward paper return over the trailing
    90 days, grouped by signal_name, refreshed weekly on the server.

    Values are clipped to [0.003, 0.015] (0.3% - 1.5%). Signal types with
    fewer than 30 historical samples in the rolling window fall through to
    a 0.5% conservative default.
    """
    exit_target: float
    """Suggested exit price in USD.

    Computed as ``entry_price * (1 + expected_return_pct)``.
    See :attr:`expected_return_pct` for the source of the multiplier.
    """
    primary_horizon: str
    horizon_end: Optional[str] = None
    """Suggested exit time, ISO 8601. Typically ``signal_time + 2h30m``,
    capped at 15:50 ET (market close − 10 min). Max tier only.
    """

    @classmethod
    def from_dict(cls, data: dict | None) -> Optional[ExecutionGuidance]:
        if not data:
            return None
        return cls(
            entry_price=data["entry_price"],
            expected_return_pct=data["expected_return_pct"],
            exit_target=data["exit_target"],
            primary_horizon=data["primary_horizon"],
            horizon_end=data.get("horizon_end"),
        )


@dataclass
class PreflightData:
    """Real-time preflight checks (Max tier only)."""

    price_vs_entry_pct: Optional[float]
    intraday_range_position: Optional[float]
    relative_volume: Optional[float]
    checked_at: str  # ISO 8601

    @classmethod
    def from_dict(cls, data: dict | None) -> Optional[PreflightData]:
        if not data:
            return None
        return cls(
            price_vs_entry_pct=data.get("price_vs_entry_pct"),
            intraday_range_position=data.get("intraday_range_position"),
            relative_volume=data.get("relative_volume"),
            checked_at=data["checked_at"],
        )


@dataclass
class Signal:
    """A single trading signal."""

    symbol: str
    direction: str
    win_rate: float
    current_price: Optional[float]
    vix_at_signal: Optional[float]
    sector: Optional[str]
    industry: Optional[str]
    execution_guidance: Optional[ExecutionGuidance] = None
    preflight: Optional[PreflightData] = None

    @classmethod
    def from_dict(cls, data: dict) -> Signal:
        return cls(
            symbol=data["symbol"],
            direction=data["direction"],
            win_rate=data["win_rate"],
            current_price=data.get("current_price"),
            vix_at_signal=data.get("vix_at_signal"),
            sector=data.get("sector"),
            industry=data.get("industry"),
            execution_guidance=ExecutionGuidance.from_dict(data.get("execution_guidance")),
            preflight=PreflightData.from_dict(data.get("preflight")),
        )


@dataclass
class SignalResponse:
    """Top-level response from GET /v1/signals."""

    market_hour: str       # ISO 8601
    signal_count: int
    tier: str
    next_update: Optional[str]  # ISO 8601 or None
    signals: list[Signal]
    disclaimer: str

    @classmethod
    def from_dict(cls, data: dict) -> SignalResponse:
        return cls(
            market_hour=data["market_hour"],
            signal_count=data["signal_count"],
            tier=data["tier"],
            next_update=data.get("next_update"),
            signals=[Signal.from_dict(s) for s in data.get("signals", [])],
            disclaimer=data.get("disclaimer", ""),
        )
