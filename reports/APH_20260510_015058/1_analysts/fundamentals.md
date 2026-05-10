## 1. Business snapshot
- APH = Technology / Electronic Components; no segment or end-market split exposed by `get_fundamentals`.
- Scale large: market cap USD 157.5B; trailing 12 months revenue USD 25.904B; net income USD 4.466B; return on equity (ROE) 36.8%; return on assets (ROA) 13.5% (`get_fundamentals`).
- Growth mix now acquisition-heavy: business purchases USD 2.156B in FY2024, USD 3.819B in FY2025, USD 10.592B in Q1 FY2026 (`get_cashflow`).
- Post-deal asset base now dominated by acquired assets: goodwill + other intangibles USD 22.944B at 2026-03-31, up from USD 12.817B at 2025-12-31 (`get_balance_sheet`).

## 2. Profitability and growth
- Q1 FY2026 revenue USD 7.620B vs USD 4.811B in Q1 FY2025 (+58.4%); gross profit USD 2.800B (+70.3%); operating income USD 1.949B (+82.3%); net income USD 933M (+26.5%) (`get_income_statement`).
- Margin stack improved at core-op level: gross margin 36.7% vs 34.2%; operating margin 25.6% vs 22.2%; net margin 12.2% vs 15.3%. Net margin lag came from tax + interest below operating line, not weak core margin (`get_income_statement`).
- FY2025 vs FY2024 step-change: revenue USD 23.095B vs USD 15.223B (+51.7%); gross margin 36.9% vs 33.8%; operating margin 25.9% vs 21.6%; net margin 18.5% vs 15.9% (`get_income_statement`).
- DuPont, trailing 12 months: 17.2% net margin × ~0.80× asset turnover × ~2.68× leverage = ~36.8% ROE (`get_fundamentals`, `get_balance_sheet`). FY2024 math was ~15.9% × ~0.80× × ~2.08× = ~26.5%; ROE lift came from margin expansion + higher leverage, not faster asset turns.

## 3. Cash flow quality
- Cash quality strong: FY2025 operating cash flow (CFO) USD 5.375B vs net income from continuing ops USD 4.305B = 1.25×; 2022-FY2025 cumulative CFO / net income ≈ 1.22× (`get_cashflow`, `get_income_statement`).
- Last four quarters through Q1 FY2026: CFO USD 5.731B; capital expenditure USD 1.100B; free cash flow (FCF) USD 4.632B; FCF margin 17.9%; capital expenditure intensity 4.2% of revenue (`get_cashflow`, `get_income_statement`).
- Q1 FY2026 still converted: CFO USD 1.122B vs net income from continuing ops USD 943M; FCF USD 830M after capital expenditure USD 292M. Working capital was a USD 507M use, so quarter had growth drag, not liquidation help (`get_cashflow`).
- Forensic check decent: accounts receivable rose 49.8% and inventory 40.6% vs revenue up 58.4% from Q1 FY2025 to Q1 FY2026; no sign receivables or inventory outran sales (`get_balance_sheet`, `get_income_statement`).
- Operating cycle improved on annual averages: days sales outstanding ~63 vs ~71, days inventory ~75 vs ~85, days payables ~56 vs ~57 from FY2024 to FY2025; cash conversion cycle improved about 17 days (`get_balance_sheet`, `get_income_statement`).
- Caveat: depreciation and amortization jumped to USD 486M in Q1 FY2026 from USD 236M in Q1 FY2025; strong CFO partly reflects larger non-cash add-backs after acquisitions (`get_cashflow`, `get_income_statement`).

## 4. Balance sheet and solvency
- Q1 FY2026 total debt USD 18.749B; cash + short-term investments USD 4.583B; net debt USD 14.621B. FY2025 net debt was USD 4.371B; jump tied to Q1 FY2026 business purchase USD 10.592B (`get_balance_sheet`, `get_cashflow`).
- Leverage manageable, not light: debt / equity 1.34×; net debt / earnings before interest, tax, depreciation, and amortization (EBITDA) about 1.8× using last four quarters; current ratio 1.71×; cash covered current debt 2.17× (`get_balance_sheet`, `get_income_statement`, `get_fundamentals`).
- Interest burden rose fast: interest expense USD 207.9M in Q1 FY2026 vs USD 76.5M in Q1 FY2025; earnings before interest and tax (EBIT) covered interest 8.9× in quarter, about 13.6× over last four quarters (`get_income_statement`).
- Asset quality weaker post-deal: goodwill + intangibles USD 22.944B = 54.5% of assets and 164% of common equity; tangible book value flipped to -USD 8.967B from +USD 596M at FY2025 (`get_balance_sheet`).
- Last four quarters: buybacks USD 750M + dividends USD 909M, covered 2.8× by FCF USD 4.632B. Yet ordinary shares at 2026-03-31 were 1.2294B vs 1.2093B at 2025-03-31 (+1.7%), and diluted average shares in Q1 FY2026 were 1.2897B vs 1.2662B (+1.9%); buybacks mostly anti-dilution (`get_cashflow`, `get_balance_sheet`, `get_income_statement`).
- Piotroski 9-point checklist: 9/9 observable on annual data; about 6/9 pass. Fail buckets = leverage up, shares up, asset turnover flat/down. Pass buckets = positive profit, positive cash flow, better margins, stronger current ratio (`get_balance_sheet`, `get_cashflow`, `get_income_statement`).

## 5. Earnings quality red flags
- No classic accrual red flag in available data: CFO beat net income in every annual period shown and in Q1 FY2026; receivables and inventory did not outrun sales; gross margin expanded, not compressed (`get_cashflow`, `get_income_statement`, `get_balance_sheet`).
- Real red flag = merger and acquisition (M&A) dependence. Q1 FY2026 purchase of business USD 10.592B; goodwill + intangibles up USD 10.128B quarter/quarter; net debt up USD 10.250B vs FY2025 (`get_cashflow`, `get_balance_sheet`).
- “Unusual” charges look recurring, not one-off: FY2024 USD 127.4M; FY2025 USD 103.4M; Q1 FY2026 USD 116.9M already (`get_income_statement`).
- Tax-rate jump: tax rate for calcs 40.0% in Q1 FY2026 vs 26.9% in Q4 FY2025 and 22.7% in Q1 FY2025; net margin fell to 12.2% even with 25.6% operating margin. Cause unknown in tool output (`get_income_statement`).
- Depreciation and amortization doubled after acquisition loading; EBITDA and cash metrics flatter than GAAP earnings. Not fraud signal; does lower quality of simple adjusted-metric story (`get_cashflow`, `get_income_statement`).

## 6. Bull case / Bear case checklists
- Bull:
  - Revenue growth stays >20% vs prior year and gross margin holds >36%.
  - Operating margin stays >25%; net margin recovers >15% once tax rate settles below 27%.
  - CFO / net income stays >1.0×; FCF margin stays >15%; capital expenditure stays <5% of revenue.
  - Net debt / EBITDA stays <2.5× and EBIT / interest stays >8×.
  - No goodwill impairment; goodwill + intangibles stay <55% of assets; diluted shares grow <1% vs prior year.
- Bear:
  - Revenue growth slips <10% vs prior year while gross margin falls <35% or operating margin <23%.
  - Tax and interest drag stay structural: tax rate >30% and quarterly interest >USD 220M without offsetting margin lift.
  - CFO / net income falls <0.9× or quarterly working-capital use exceeds USD 0.8B.
  - Net debt / EBITDA rises >3.0× or EBIT / interest falls <6×.
  - Another large acquisition pushes goodwill + intangibles >60% of assets, triggers impairment, or diluted shares rise >2% vs prior year.

## 7. Unknowns and data gaps
- No segment mix, end-market mix, organic vs acquired growth split, backlog, or customer concentration in tool output.
- No debt maturity ladder, coupon schedule, or covenant detail; refinancing wall unknown.
- No disclosure behind Q1 FY2026 40.0% tax-rate spike; cannot tell one-time item vs new run-rate.
- Precise post-deal return on invested capital not clean enough: invested capital available, but acquisition step-change plus noisy tax/unusual items make comparison low-confidence.
- `get_fundamentals` shows FCF USD 3.564B, while last four quarterly `get_cashflow` periods sum to USD 4.632B. Methodology mismatch unknown; statement-derived cash flow used above.

## 8. Actionable takeaways and watchlist metrics
- APH core operating momentum stronger than headline net income: Q1 FY2026 revenue +58.4%, operating income +82.3%, operating margin 25.6%; headline net margin only 12.2% because tax rate hit 40.0% and interest expense rose 171.8%. [Conf: Med]
- Cash conversion real, not accrual mirage: FY2025 CFO / net income 1.25×; last four quarters ~1.28×; receivables and inventory grew slower than revenue. Bear case should attack integration, not stuffing. [Conf: High]
- Balance-sheet regime changed in one quarter: Q1 FY2026 business purchase USD 10.592B pushed net debt to USD 14.621B and goodwill + intangibles to 54.5% of assets. Biggest risk now = impairment/deleveraging, not near-term liquidity. [Conf: High]
- Buybacks not shrinking float: last four quarters repurchases USD 750M, yet ordinary shares still rose 1.7% vs prior year; per-share compounding weaker than absolute profit growth. [Conf: High]
- Recurring special charges plus doubled amortization mean adjusted earnings need haircut; cash still good, but post-deal accounting quality less clean than simple EBITDA story. [Conf: Med]
- Solvency still acceptable today: current ratio 1.71×, cash > current debt, EBIT / interest about 13.6× over last four quarters. If next quarter shows deleveraging without margin loss, bear case weakens fast. [Conf: High]

- Watchlist:
  - Tax rate: healthy if <27%; warning if >30% again.
  - Gross margin / operating margin: healthy if >36% / >25%; warning if <35% / <23%.
  - CFO / net income: healthy if >1.0×; warning if <0.9× or working-capital use >USD 0.8B in quarter.
  - Net debt / EBITDA and EBIT / interest: healthy if <2.0× and >8×; warning if >2.5× or <6×.
  - Goodwill + intangibles / assets: healthy if ≤55%; warning if >60% or any impairment charge.
  - Diluted share count: healthy if growth <1% vs prior year; warning if growth >2%.

## 9. Summary table
| Dimension | Evidence (figure or ratio) | Trend | Risk level | Notes |
|---|---|---|---|---|
| Growth | Q1 FY2026 revenue USD 7.620B (+58.4% vs Q1 FY2025); FY2025 revenue USD 23.095B (+51.7% vs FY2024) | Up | Med | Strong growth, but acquisition-assisted |
| Profitability / returns | FY2025 gross margin 36.9%, operating margin 25.9%, net margin 18.5%; trailing-12-month ROE 36.8% | Up | Med | ROE uplift came from margin + leverage |
| Cash conversion | FY2025 CFO / net income 1.25×; last-four-quarter FCF margin 17.9% | Strong | Low | No accrual stress visible |
| Working capital | Days sales outstanding ~63 vs ~71; days inventory ~75 vs ~85 from FY2024 to FY2025 | Better | Low | No receivables/inventory bloat |
| Leverage / liquidity | Q1 FY2026 net debt USD 14.621B; debt / equity 1.34×; current ratio 1.71×; EBIT / interest ~13.6× last four quarters | Worse | Med | Manageable now; needs deleveraging |
| Asset quality / integration | Goodwill + intangibles USD 22.944B = 54.5% of assets; tangible book -USD 8.967B | Worse | High | Post-deal impairment/integration key risk |
| Capital allocation / per-share | Last four quarters buybacks USD 750M + dividends USD 909M; ordinary shares +1.7% vs prior year | Mixed | Med | Returns covered by FCF; buybacks mostly anti-dilution |
| Earnings quality adjustments | “Unusual” charges USD 103.4M FY2025 and USD 116.9M Q1 FY2026; tax rate 40.0% in Q1 FY2026 | Mixed | Med | Adjusted metrics need skepticism |