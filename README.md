# irrationalsignals

> **⚠️ Discontinued — this project is no longer maintained.**
>
> IrrationalSignals was wound down in May 2026. The API at `api.irrationalsignals.com` is
> offline, so this SDK no longer functions against a live service. The repository stays
> public as a portfolio reference. No support, no further releases.

## What this was

IrrationalSignals was a stock-signal service. Statistical models scanned hundreds of US
equities every hour and surfaced the ones showing a measurable edge. Each signal carried a
direction, a historical win rate, an entry price, an exit target, and an expected return,
delivered over a JSON API so subscribers could automate against it.

Coverage was limited to Technology, Consumer Cyclical, and Communication Services — the
three sectors where the models held up under backtesting. Signals refreshed six times per
trading day during market hours (10:50 AM to 3:50 PM ET).

This repository is the official Python SDK: a thin, dependency-light wrapper over a single
endpoint (`GET /v1/signals`), with typed response models and mapped error classes.

## Usage (historical)

The examples below document how the SDK worked while the service was running. They will
now fail with a connection error.

```python
from irrationalsignals import Client

client = Client("isk_pro_abc123...")
response = client.get_signals()

for signal in response.signals:
    print(f"{signal.symbol} {signal.direction} (win rate: {signal.win_rate:.0%})")
```

Filtering by sector:

```python
response = client.get_signals(sector="Technology")
```

Same-day historical hour (Max tier):

```python
response = client.get_signals(hour=14)  # 2 PM ET signals
```

Error handling:

```python
from irrationalsignals import Client, AuthError, RateLimitError, APIError

client = Client("isk_pro_abc123...")

try:
    response = client.get_signals()
except AuthError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limited — retry after {e.retry_after}s")
except APIError as e:
    print(f"API error {e.status_code}: {e.detail}")
```

## Response Objects

### `SignalResponse`

| Field | Type | Description |
|-------|------|-------------|
| `market_hour` | `str` | ISO 8601 UTC timestamp of the signal hour |
| `signal_count` | `int` | Number of signals returned |
| `tier` | `str` | Plan tier (`free`, `pro`, `max`) |
| `next_update` | `str \| None` | When the next signal batch was expected |
| `signals` | `list[Signal]` | The signals |
| `disclaimer` | `str` | Legal disclaimer |

### `Signal`

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | `str` | Ticker symbol |
| `direction` | `str` | `"BUY"` |
| `win_rate` | `float` | Historical win rate (0–1) |
| `current_price` | `float \| None` | Latest price |
| `vix_at_signal` | `float \| None` | VIX level when signal was generated |
| `sector` | `str \| None` | GICS sector |
| `industry` | `str \| None` | GICS industry |
| `execution_guidance` | `ExecutionGuidance \| None` | Entry/exit targets |
| `preflight` | `PreflightData \| None` | Real-time checks (Max only) |

### `ExecutionGuidance`

| Field | Type | Tier |
|-------|------|------|
| `entry_price` | `float` | All |
| `expected_return_pct` | `float` | All |
| `exit_target` | `float` | All |
| `primary_horizon` | `str` | All |
| `stop_loss_armed` | `float \| None` | Max |
| `stop_loss_hard` | `float \| None` | Max |
| `horizon_end` | `str \| None` | Max |

### `PreflightData` (Max tier only)

| Field | Type | Description |
|-------|------|-------------|
| `price_vs_entry_pct` | `float \| None` | Price drift from entry |
| `intraday_range_position` | `float \| None` | Position in day's range (0–1) |
| `relative_volume` | `float \| None` | Volume vs. average |
| `checked_at` | `str` | ISO 8601 timestamp |

## Tiers (as offered)

| Feature | Free | Pro | Max |
|---------|------|-----|-----|
| Signals per hour | 1 | 8 | Unlimited |
| Market hours | 10 AM only | All hours | All hours |
| Execution guidance | Basic | Basic | Full (+ stop losses) |
| Preflight data | — | — | Included |
| Historical lookback | — | — | Same-day by hour |
| Daily API calls | 25 | 100 | 500 |

## License

MIT. See `pyproject.toml`.
