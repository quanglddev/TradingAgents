# APH Technical Analysis — Market Analyst Report

Date: 2026-05-10 | Ticker: APH | Data through: 2026-05-08 (last trading day)

---

## 1. Regime

**STRONG_DOWNTREND**

Evidence:
- Price (128.03) closed below 200-SMA (131.64) and 50-SMA (136.92), both now acting as overhead resistance. 50-SMA slope is declining — fell from 143.57 on Mar 11 to 136.92 on May 8. [Conf: High]
- Price broke below lower Bollinger Band (132.59) on May 8, closing 4.56 pts beneath it. Band expansion (boll_ub − boll_lb = 25.31) confirms volatility supporting trend, not mean-reversion compression. [Conf: High]
- MACD line crossed below zero between May 7 (+0.42) and May 8 (−0.73) — fresh bearish momentum signal. RSI at 34.65, not yet oversold, implying room for further downside before exhaustion. [Conf: High]
- Volume on May 8: 18.07M shares vs ~7–9M average — selling with conviction. Price well below VWMA (143.19), confirming distribution. [Conf: Med]

---

## 2. Indicator Readout

### 2.1 close_50_sma
- Latest: 136.92 (May 8)
- Implication: Medium-term trend is bearish; price is -6.5% below the 50-SMA. SMA slope has been declining for 2 months. Until price reclaims this level, trend structure remains lower highs / lower lows.
- Conflict: 50-SMA still above 200-SMA (golden cross structure technically intact), but price is below both — a "cross abandoned" setup where the golden cross signal has been negated by price action.

### 2.2 close_200_sma
- Latest: 131.64 (May 8)
- Implication: Long-term trend benchmark now broken to the downside. The 200-SMA is still rising slowly (was ~123 in mid-March, now 131.64), so the long-term slope is positive — but price has decisively undercut it. This creates a bearish divergence: rising 200-SMA vs falling price.
- Conflict: Rising 200-SMA could act as a magnet for mean reversion. Historically, first breaks of a rising 200-SMA often get retested.

### 2.3 macd
- Latest: −0.73 (May 8)
- Implication: MACD line just crossed below zero. Peak was +4.85 on Apr 23; the decline from +4.85 to −0.73 in 11 trading days represents rapid momentum decay. This is a fresh bearish crossover of the zero line.
- No macds/macdh data available for signal-line cross confirmation — using zero-line cross as primary MACD signal.

### 2.4 rsi
- Latest: 34.65 (May 8)
- Implication: Approaching oversold (30 threshold) but not there yet. RSI has dropped from 68.58 (Apr 20) to 34.65 in 14 sessions — steep momentum loss without capitulation. Headroom remains for further downside before oversold bounce.
- Relation to MACD: Both agree on bearish momentum — no divergence.

### 2.5 boll_ub / boll_lb
- boll_ub: 157.90 | boll_lb: 132.59 (May 8)
- Implication: Price closing below the lower band (132.59) is a breakout/breakdown signal, not a mean-reversion tag. Band width (25.31) is elevated, consistent with trending volatility. In strong trends, price can ride outside the band for multiple sessions.
- Prior instances of closing below lower band: check price action around Mar 30–Apr 1 period when price was near 119–127 area — similar pattern preceded a bounce.

### 2.6 atr
- Latest: 5.95 (May 8)
- Implication: ATR elevated and rising — was ~5.0 in late April, now near 6.0. This is roughly 4.6% of price (128.03). High ATR demands wider stops and smaller position sizing.
- Trend regime + elevated ATR = stops placed at 1.5×ATR risk being whipsawed. Sizing note: position size should be reduced by factor of ~1.3× vs normal-vol regimes.

### 2.7 vwma
- Latest: 143.19 (May 8)
- Implication: Volume-weighted average confirms distribution — price is 15.16 pts (10.6%) below VWMA. The VWMA has declined from 148.63 (May 1) to 143.19, confirming selling pressure is volume-backed, not just low-volume drift.
- Consistent with bearish MACD and price < all MAs.

---

## 3. Key Levels and Risk Geometry

| Level | Price | Role |
|---|---|---|
| Resistance 3 | 143.19 | VWMA — volume-weighted ceiling |
| Resistance 2 | 136.92 | 50-SMA — medium-term trend resistance |
| Resistance 1 | 132.59 | Lower Bollinger Band / 200-SMA cluster (131.64–132.59) |
| **Current** | **128.03** | Last close |
| Support 1 | 127.35 | Mar 3 swing low |
| Support 2 | 119.15 | Mar 30 swing low — major structural floor |

**Invalidation level (bearish thesis):** Close above 136.92 (50-SMA) would falsify the downtrend structure. A close above 132.59 (lower BB) alone is insufficient — would merely signal mean reversion inside the band, not trend change.

**ATR-aware stop suggestion:**
- For short entries: stop at 136.93 (entry + 1.5×ATR of 5.95), which conveniently aligns with the 50-SMA.
- For counter-trend long entries: stop at 119.10 (entry − 1.5×ATR), just below the Mar 30 structural low.
- Position sizing: reduce to 65–75% of normal size given ATR at 4.6% of price.

---

## 4. Scenarios

### Bull Case (counter-trend)
- Setup: Mean reversion from below lower Bollinger band. Rising 200-SMA acts as gravitational pull.
- Trigger: Daily close back above 132.59 (lower BB).
- Target: 136–138 zone (50-SMA area).
- Invalidation: Break below 127.35 (Mar 3 low) with volume.

### Bear Case (trend continuation)
- Setup: Momentum breakdown continues; price rides below lower BB for multiple sessions.
- Trigger: Already active — price below lower BB, MACD negative, RSI declining.
- Target: 119–120 zone (Mar 30 structural low). Secondary target: 115 area if that fails.
- Invalidation: Close above 132.59 with follow-through above 136.92.

### Base Case (most probable)
- Setup: Short-term oversold bounce toward 200-SMA / lower BB cluster (131–133), sellers re-emerge, downtrend resumes.
- Trigger: RSI approaching 30 triggers mechanical bounce; price tags 131–133 zone.
- Target: Bounce fades at 131–133, resumption toward 119–125 range.
- Invalidation: If bounce clears 136.92 and holds, reassess to WEAK_DOWNTREND or RANGE.

---

## 5. Unknowns and Data Gaps

- MACD signal line (macds) and histogram (macdh) not retrieved — zero-line cross used as proxy; signal-line crossover timing is unconfirmed.
- No close_10_ema data — fast momentum context missing; unable to assess short-term mean-reversion triggers precisely.
- May 8 volume spike (18.07M) may contain one-off institutional flow or options expiry effects — single-session volume anomalies can mislead.
- No fundamental or news context — the Jan 28 crash (37.79M volume, −12.2% intra-range) and Feb 4 crash (21.25M volume, −11.6%) suggest event-driven moves; technicals alone incomplete.

---

## 6. Actionable Takeaways

- Price closed below all major MAs (50-SMA 136.92, 200-SMA 131.64) and below lower Bollinger Band (132.59) — bearish on all structural timeframes. [Conf: High]
- MACD crossed below zero line on May 8 (−0.73) after peaking at +4.85 on Apr 23 — momentum collapse of ~5.6 MACD points in 11 sessions signals strong institutional distribution. [Conf: High]
- RSI at 34.65 not yet oversold — downside headroom exists before mechanical bounce. No bullish divergence. [Conf: Med]
- ATR at 5.95 (4.6% of price) demands wider stops. 1.5×ATR stop for shorts = 136.93; aligns almost exactly with 50-SMA. [Conf: High]
- VWMA at 143.19 vs price 128.03 confirms volume-backed selling. Gap of 10.6% is extreme — mean reversion odds increase as gap widens, but timing is uncertain. [Conf: Med]
- 200-SMA still rising (131.64) despite price below it — this divergence historically resolves either by price recovering toward SMA or SMA rolling over. Watch 200-SMA slope for regime-confirmation signal. [Conf: Med]
- Next major support is 119.15 (Mar 30 low). If that breaks, no structural support until ~110–112 zone (pre-Oct 2025 levels). [Conf: Med]

---

## 7. Second-Order Notes

- **Indicator disagreements:** Rising 200-SMA conflicts with bearish price action. 50-SMA still above 200-SMA (golden cross intact technically), but price below both — this "bullish MA structure + bearish price" pattern often precedes a 200-SMA slope rollover. If 200-SMA flattens or turns down in next 2–3 weeks, confirms secular trend change.
- **False-signal traps:** Closing below lower Bollinger Band often triggers mean-reversion buyers — in strong downtrends, these bounces are shallow and fail at the band. Do not fade the breakdown until RSI divergence or bullish MACD cross appears.
- **Regime-change tripwires:**
  - Bullish regime shift: price reclaims 136.92 (50-SMA) on weekly close + MACD crosses back above zero.
  - Range-bound shift: price stabilizes between 127–137 for 5+ sessions with ATR contracting toward 4.0.
  - Downtrend acceleration: break of 119.15 with volume >12M shares.
- **Volume anomaly:** May 8 volume (18.07M) was 2.5× average. Previous volume spikes at capitulation lows (Mar 30: ~8.2M was modest; Jan 28: 37.8M was extreme). Current volume profile looks more like distribution than capitulation — no climactic washout yet.

---

## 8. Summary Table

| Signal | Evidence | Bull/Bear tilt | Confidence | Notes |
|---|---|---|---|---|
| Price vs 50-SMA | 128.03 vs 136.92, −6.5%, SMA declining | Bearish | High | Medium-term trend is down |
| Price vs 200-SMA | 128.03 vs 131.64, −2.7%, 200-SMA still rising | Bearish | High | Rising 200-SMA adds mean-reversion risk |
| MACD zero-line cross | −0.73, crossed negative May 8 from +4.85 peak Apr 23 | Bearish | High | Fresh bearish momentum signal |
| RSI | 34.65, not yet oversold, no divergence | Bearish | Med | Room to fall before mechanical bounce |
| Lower Bollinger break | Close 128.03 below lower BB 132.59 | Bearish | High | Riding band in strong trend |
| ATR expansion | 5.95 (4.6% of price), rising from ~5.0 in late April | Bearish | Med | Elevated vol supports trend, hurts mean-reversion |
| VWMA gap | Price 10.6% below VWMA (143.19), VWMA declining | Bearish | High | Volume confirms distribution |
| Volume | May 8: 18.07M (2.5× avg), no capitulation signature | Bearish | Med | Distribution, not washout |