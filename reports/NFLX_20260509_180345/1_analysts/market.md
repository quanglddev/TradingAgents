# NFLX Technical Analysis — 2026-05-09

## 1. Regime

**STRONG_DOWNTREND**

- Price ($87.49) sits below all major moving averages: VWMA ($91.23), 50 SMA ($95.54), 200 SMA ($103.34). Distance from 200 SMA is -15.3% — deep bear territory.
- Death cross confirmed: 50 SMA ($95.54) well below 200 SMA ($103.34), gap widening (~$7.80 spread). Both SMAs sloping down.
- MACD at -2.15 and accelerating negative (was -0.98 on May 1, -1.17 on May 4, -1.55 on May 5). No histogram convergence visible.
- RSI at 33.89 — not yet oversold (<30), still has room to fall. Prior bounce attempts (Apr 28–30, RSI 41→45) failed to reclaim VWMA.
- High-volume distribution events: Apr 17 (125.9M shares, -$10.48), May 5 (51.9M shares, -$3.13). Volume confirms selling pressure.

## 2. Indicator readout

### close_50_sma — $95.54 (May 8)
Sloping down from $97+ a month ago. Price has not touched 50 SMA since Apr 16–17 breakdown. Acts as overhead resistance — any rally that fails below this level keeps the trend intact. Gap from price: $8.05 (9.2%).

### close_200_sma — $103.34 (May 8)
Long-term bearish benchmark. Steady decline from $113.23 (Jan 9) to $103.34 — losing ~$10 in 4 months. Price hasn't been above 200 SMA since late Feb 2026. Death cross (50 < 200) originated approximately late Feb/early Mar and continues to widen. No golden cross setup visible.

### rsi — 33.89 (May 8)
Near oversold but not there. RSI has been trapped in 33–42 range for past two weeks (5 sessions: 33.9, 35.3, 35.3, 34.2, 39.8). No bullish divergence — RSI making lower lows alongside price. If price breaks below $87, RSI likely enters sub-30 oversold, but in strong downtrends RSI can stay oversold for extended periods.

### macd — -2.15 (May 8)
Deeply negative and widening. Crossed below signal line around Apr 22–24 (MACD went from +1.67 on Apr 21 to +0.11 on Apr 24, negative thereafter). Rate of decline accelerating: -0.98 (May 1) → -1.17 (May 4) → -1.55 (May 5) → -1.80 (May 6) → -1.98 (May 7) → -2.15 (May 8). No histogram trough visible — momentum still deteriorating.

### boll_ub / boll_lb — $107.56 / $81.69 (May 8)
Band width: $25.87 (~29.6% of price). Extremely wide, consistent with high-volatility regime. Price hugging the lower half of the band envelope after the Apr 17 breakdown. Lower band ($81.69) is declining ~$0.50–0.75/day — dynamic support sliding lower. Upper band flat-to-slightly declining — no squeeze setup.

### atr — $2.57 (May 8)
Elevated. Recent trajectory: peaked at $3.52 (Apr 20–21), now settling to $2.57 but still above pre-Apr levels (~$2.80 area). Represents ~2.94% daily range. Elevated ATR in a downtrend means wide stop requirements and reduced position sizing.

### vwma — $91.23 (May 8)
Price ($87.49) is $3.74 below VWMA — bearish volume confirmation. VWMA has been declining steadily (was $100.04 on Apr 17, now $91.23). Moving average of volume-weighted prices shows sellers dominating. No session has closed above VWMA since Apr 17.

**Conflicts:** No material conflicts. Every indicator points bearish. Only nuance: RSI not yet oversold leaves room for further decline without mean-reversion signal.

## 3. Key levels and risk geometry

| Level | Price | Role |
|---|---|---|
| Resistance 3 | $103.34 | 200 SMA — structural bear/bull boundary |
| Resistance 2 | $95.54 | 50 SMA — tactical resistance |
| Resistance 1 | $91.23 | VWMA — first hurdle for any bounce |
| **Current** | **$87.49** | Last close |
| Support 1 | $85.00 | Psychological round number / recent swing low area |
| Support 2 | $81.69 | Bollinger lower band (dynamic, declining) |
| Support 3 | $75.86 | Feb 12 low — major swing low |

**Invalidation level:** A daily close above the 50 SMA ($95.54) would falsify the strong-downtrend hypothesis. A close above VWMA ($91.23) would be a first warning that bear momentum is weakening.

**ATR-aware stop:** For a short entry near current price ($87.49), a stop at $91.35–$91.50 covers 1.5× ATR ($3.86). For a counter-trend long attempting to catch an oversold bounce, stop below $85.00 (1.0× ATR under entry) given range-like lower-bound behavior.

**Position sizing note:** HIGH_VOL regime (ATR 2.94% of price, BB width ~30%). Reduce position size by 30–50% vs. normal. Wide bands mean stops must be wider in dollar terms.

## 4. Scenarios

### Bull case (counter-trend)
- **Setup:** RSI reaches oversold (<30) in coming days, price touches or nears lower Bollinger band ($81.69), forms a hammer or bullish engulfing on daily.
- **Trigger:** Close back above $89.00 (recapture of May 5 breakdown level) with RSI hooking up from oversold.
- **Target:** VWMA ($91.23), then 50 SMA ($95.54).
- **Invalidation:** New low below $81.69 (lower BB break) or failure to close above VWMA within 3–5 sessions.

### Bear case (trend continuation)
- **Setup:** Current trend intact. No bullish divergence. MACD still accelerating down. Price rejected from VWMA or 50 SMA repeatedly.
- **Trigger:** Break below $87.00 with volume, or a failed bounce at VWMA ($91.23).
- **Target:** Lower Bollinger band ($81.69), then the Feb 12 swing low ($75.86).
- **Invalidation:** Close above 50 SMA ($95.54).

### Base case (orderly decline with intermittent oversold bounces)
- **Setup:** Price grinds lower within the wide Bollinger bands. Occasional RSI-oversold bounces to VWMA or 50 SMA that fail and resume the trend.
- **Trigger:** VWMA ($91.23) acts as a descending ceiling. Each bounce caps below it.
- **Target:** Gradual descent toward $81–$83 over the next 2–4 weeks as lower BB slides down.
- **Invalidation:** Two consecutive daily closes above 50 SMA or a MACD bullish crossover.

## 5. Unknowns and data gaps

- **close_10_ema not retrieved.** Chose VWMA for volume confirmation instead. Short-term EMA slope and cross behavior vs. 50 SMA unobserved — would sharpen entry timing.
- **MACD signal line (macds) and histogram (macdh) not separately retrieved.** Using MACD line trajectory as proxy for momentum direction. Signal-line cross precision unavailable.
- **No pre-April 9 indicator data for 50 SMA, RSI, MACD, BB, ATR, VWMA** (30-day lookback limit on those calls). Pre-April price action reconstructed from OHLCV only.
- **Stock split (10:1 on Nov 17, 2025):** Prices appear split-adjusted throughout the OHLCV series. No discontinuity in adjusted data. Exact split-adjustment methodology not verified.

## 6. Actionable takeaways

- NFLX in confirmed death cross: 50 SMA ($95.54) below 200 SMA ($103.34), both declining — structural bear trend with no reversal signal. [Conf: High]
- Price ($87.49) trades below all key MAs and VWMA ($91.23). Every bounce in the last 3 weeks failed at or below VWMA. [Conf: High]
- MACD at -2.15 and still accelerating downward — no momentum divergence, no histogram trough. Trend strength increasing, not fading. [Conf: High]
- RSI at 33.89 is near but not at oversold. Prior oversold bounces (RSI 34–35 → 41–45) failed to clear VWMA. Oversold alone is not a buy signal in this regime. [Conf: Med]
- Lower Bollinger band at $81.69 and declining — dynamic support not yet tested. A move to $81–$83 would complete a mean-reversion touch without breaking trend structure. [Conf: Med]
- 1.5× ATR stop above entry = ~$3.86 from current $87.49. In this volatility regime, position size should be reduced 30–50% vs. normal. [Conf: Med]
- Regime-change tripwire: daily close above $95.54 (50 SMA). First warning: close above $91.23 (VWMA). Until then, counter-trend longs are low-probability. [Conf: High]

## 7. Second-order notes

- **Where indicators disagree:** None disagree. Unanimous bearish alignment — rare. This level of agreement increases conviction but also raises the risk of a sharp mean-reversion snap when sentiment exhausts.
- **False-signal traps for STRONG_DOWNTREND:**
  - RSI oversold bounces that fail at VWMA/50 SMA — classic bull trap. Wait for confirmation above VWMA before assuming reversal.
  - Bollinger lower-band tag alone is not a buy signal without bullish candle confirmation and RSI divergence.
  - Volume dry-up on green days vs. heavy volume on red days — bearish continuation signal, not accumulation.
- **Regime-change tripwires:**
  - Primary: Close above 50 SMA ($95.54) → downgrades to WEAK_DOWNTREND or RANGE.
  - Early warning 1: Close above VWMA ($91.23) sustained for 2+ sessions.
  - Early warning 2: MACD histogram trough and bullish crossover (MACD crossing above signal line).
  - Early warning 3: RSI bullish divergence — higher RSI low alongside lower price low.
- **ATR trend note:** ATR declining from $3.52 to $2.57 over 3 weeks — volatility compression within the downtrend. If ATR stabilizes around $2.00–$2.20, regime may shift toward LOW_VOL_COMPRESSION or RANGE.

## 8. Summary table

| Signal | Evidence | Bull/Bear tilt | Confidence | Notes |
|---|---|---|---|---|
| Death cross (50 < 200 SMA) | 50 SMA $95.54 vs 200 SMA $103.34, both declining | Bear | High | Gap widening, no convergence |
| Price vs MAs | Close $87.49 below VWMA ($91.23), 50 SMA ($95.54), 200 SMA ($103.34) | Bear | High | -15.3% from 200 SMA |
| MACD momentum | -2.15, accelerating negative daily | Bear | High | Rate of decline increasing |
| RSI | 33.89, not yet oversold | Bear | Med | Room to fall; prior bounces failed |
| VWMA confirmation | Price $3.74 below VWMA, VWMA declining | Bear | High | Sellers control volume-weighted price |
| Bollinger bands | Width $25.87 (~30%), price near lower half | Bear | Med | Lower band sliding down, no squeeze |
| ATR volatility | $2.57 (2.94% of price), declining from $3.52 spike | Neutral | Med | High vol = wide stops, reduced size |