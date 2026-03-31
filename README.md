# irrationalsignals

**Know what to trade before the market does.**

Statistical models scan hundreds of US equities every hour and surface the ones with a measurable edge. Every signal includes a direction, historical win rate (70%+ average), entry price, exit target, and expected return — delivered via API so you can automate it or use it however you want.

IrrationalSignals covers Technology, Consumer Cyclical, and Communication Services — three sectors where the models have demonstrated statistical edge. Signals update 6 times per trading day during market hours (10:50 AM to 3:50 PM ET).

This is the official Python SDK. Get started in under a minute.

```
pip install irrationalsignals
```

## Quick Start

```python
from irrationalsignals import Client

client = Client("isk_pro_abc123...")
response = client.get_signals()

for signal in response.signals:
    print(f"{signal.symbol} {signal.direction} (win rate: {signal.win_rate:.0%})")
```

## Filter by Sector

```python
response = client.get_signals(sector="Technology")
```

## Historical Hour (Max Tier)

```python
response = client.get_signals(hour=14)  # 2 PM ET signals
```

## Error Handling

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
| `tier` | `str` | Your plan tier (`free`, `pro`, `max`) |
| `next_update` | `str \| None` | When the next signal batch is expected |
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

## Tier Comparison

| Feature | Free | Pro | Max |
|---------|------|-----|-----|
| Signals per hour | 1 | 8 | Unlimited |
| Market hours | 10 AM only | All hours | All hours |
| Execution guidance | Basic | Basic | Full (+ stop losses) |
| Preflight data | — | — | Included |
| Historical lookback | — | — | Same-day by hour |
| Daily API calls | 25 | 100 | 500 |

## Links

- [Website](https://irrationalsignals.com)
- [Full API documentation](https://irrationalsignals.com/docs)
- [Pricing](https://irrationalsignals.com/pricing)
- [Dashboard & API keys](https://irrationalsignals.com/dashboard)
- [Get a free API key](https://irrationalsignals.com/register)
