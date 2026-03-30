"""Dataclass models matching the IrrationalSignals API response."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class ExecutionGuidance:
    """Entry/exit targets and risk levels for a signal."""

    entry_price: float
    expected_return_pct: float
    exit_target: float
    primary_horizon: str
    stop_loss_armed: Optional[float] = None   # Max tier only
    stop_loss_hard: Optional[float] = None     # Max tier only
    horizon_end: Optional[str] = None          # Max tier only — ISO 8601

    @classmethod
    def from_dict(cls, data: dict | None) -> Optional[ExecutionGuidance]:
        if not data:
            return None
        return cls(
            entry_price=data["entry_price"],
            expected_return_pct=data["expected_return_pct"],
            exit_target=data["exit_target"],
            primary_horizon=data["primary_horizon"],
            stop_loss_armed=data.get("stop_loss_armed"),
            stop_loss_hard=data.get("stop_loss_hard"),
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
