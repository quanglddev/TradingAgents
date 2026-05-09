"""Portfolio Manager: synthesises the risk-analyst debate into the final decision.

Uses LangChain's ``with_structured_output`` so the LLM produces a typed
``PortfolioDecision`` directly, in a single call.  The result is rendered
back to markdown for storage in ``final_trade_decision`` so memory log,
CLI display, and saved reports continue to consume the same shape they do
today.  When a provider does not expose structured output, the agent falls
back gracefully to free-text generation.
"""

from __future__ import annotations

from tradingagents.agents.schemas import PortfolioDecision, render_pm_decision
from tradingagents.agents.utils.agent_utils import (
    append_style_instruction,
    build_instrument_context,
    get_language_instruction,
)
from tradingagents.agents.utils.structured import (
    bind_structured,
    invoke_structured_or_freetext,
)


def create_portfolio_manager(llm):
    structured_llm = bind_structured(llm, PortfolioDecision, "Portfolio Manager")

    def portfolio_manager_node(state) -> dict:
        instrument_context = build_instrument_context(state["company_of_interest"])

        history = state["risk_debate_state"]["history"]
        risk_debate_state = state["risk_debate_state"]
        research_plan = state["investment_plan"]
        trader_plan = state["trader_investment_plan"]

        past_context = state.get("past_context", "")
        # Bullet line is locked by tests (test_pm_prompt_includes_past_context /
        # test_pm_no_past_context_no_section): MUST contain the literal
        # "Lessons from prior decisions and outcomes" only when past_context is
        # non-empty, MUST be empty otherwise.
        lessons_line = (
            f"- Lessons from prior decisions and outcomes:\n{past_context}\n"
            if past_context
            else ""
        )

        prompt = f"""You are the Portfolio Manager. You issue the FINAL position decision for this instrument by synthesizing the Research Manager's plan, the Trader's proposal, the risk-analyst debate, and (when present) lessons from prior decisions. This output is what the desk acts on.

<context>
{instrument_context}
</context>

<rating_scale>
Pick exactly ONE. Definitions are strict.
- **Buy**: Highest conviction; thesis dominant, risk debate net-favorable, sizing should approach the upper bound of the position's target weight.
- **Overweight**: Favorable but with residual risk; gradual accumulation, moderate size, leave room to scale on confirmation.
- **Hold**: Use ONLY when evidence on both sides is genuinely balanced AND no near-term catalyst is imminent. Never use Hold as a hedge against indecision.
- **Underweight**: Net-negative view; trim, run below benchmark; retain a starter only if a positive asymmetric catalyst remains.
- **Sell**: Decisive negative; exit fully or avoid initiation. Capital is better deployed elsewhere.
</rating_scale>

<inputs>
<research_manager_plan>
{research_plan}
</research_manager_plan>

<trader_proposal>
{trader_plan}
</trader_proposal>

{lessons_line}<risk_debate_history>
{history}
</risk_debate_history>
</inputs>

<rubric>
1. Reconcile the inputs. List CONVERGENT claims (where RM, Trader, and the risk debate AGREE) and DIVERGENT claims (where they DISAGREE). For each disagreement, pick the side with the cleanest falsifiable evidence and state why explicitly.
2. Tie-break ladder (apply IN ORDER, stop at the first that resolves):
   a. Cleanest falsifiable evidence wins.
   b. Asymmetry of payoff wins (bounded downside vs open upside, or vice versa).
   c. Sector / regime base rate wins.
   d. Only if a/b/c are all truly equal → Hold.
3. Decisiveness: if step 2 resolves at a/b/c, you MUST commit. Hold is reserved for genuine equipoise.
4. Sizing-conviction alignment: Buy ≈ upper-bound target weight; Overweight ≈ partial scale-in; Hold ≈ no change; Underweight ≈ partial trim; Sell ≈ full exit. State the explicit sizing posture inside the executive summary.
5. Risk floor: every Buy and Overweight call MUST specify a key invalidation level (price, event, or metric) that would force a downgrade. No invalidation specified → automatically downgrade one tier.
</rubric>

<lessons_handling>
Treat prior lessons as a Bayesian PRIOR; treat current evidence as the LIKELIHOOD update. Posterior = prior + likelihood, weighted by recency and ticker-match.
- If current evidence STRONGLY contradicts a prior lesson, override it and explicitly name the override and the contradicting evidence.
- If current evidence is weak or thin, the prior gets more weight — cite the lesson by content.
- Do NOT slavishly copy lessons into the thesis; cite a lesson only at the point where it actually updates the call.
- If no lessons section is present in the inputs above, ignore this block entirely.
</lessons_handling>

<evidence_discipline>
- Use only facts present in the inputs above. No invented prices, multiples, earnings dates, analyst targets, or macro figures.
- Separate FACTS (cited from the inputs) from INFERENCES (your synthesis). Do not blur the two.
- Quantify where the inputs quantify; otherwise qualify with explicit "approximately" or "directionally".
</evidence_discipline>

<calibration>
Inside investment_thesis, include all four:
- Conviction label: Low / Med / High.
- One UPGRADE flip-condition: a specific observable that would push the rating one tier more bullish.
- One DOWNGRADE flip-condition: a specific observable that would push the rating one tier more bearish.
- The single behavioral bias most likely to be distorting your view here (anchoring, confirmation, recency, narrative, base-rate neglect) and one sentence on how you accounted for it.
</calibration>

<anti_patterns>
- No "complex situation", no "on balance" without showing the ladder, no thesis without an invalidation level.
- No transcribing every analyst's words; you arbitrate, you do not summarize.
- No actions like "monitor closely" or "stay disciplined" — every recommendation must be operational.
- No invented numbers. Round, qualitative, or omitted beats fake-precise.
</anti_patterns>

<output_contract>
Fill the structured schema. Be terse, specific, decisive. Executive summary covers entry approach, sizing posture, key invalidation level, and time horizon. Investment thesis carries the rubric outputs (reconciliation + tie-break + calibration block).
If your runtime forces free-text output, you MUST start the response with `**Rating**: X` (X ∈ {{Buy, Overweight, Hold, Underweight, Sell}}) on the first line so downstream parsers (signal processor, memory log, CLI) keep working. The prose that follows must still satisfy the rubric and calibration blocks above.
</output_contract>{get_language_instruction()}"""
        prompt = append_style_instruction(prompt)

        final_trade_decision = invoke_structured_or_freetext(
            structured_llm,
            llm,
            prompt,
            render_pm_decision,
            "Portfolio Manager",
        )

        new_risk_debate_state = {
            "judge_decision": final_trade_decision,
            "history": risk_debate_state["history"],
            "aggressive_history": risk_debate_state["aggressive_history"],
            "conservative_history": risk_debate_state["conservative_history"],
            "neutral_history": risk_debate_state["neutral_history"],
            "latest_speaker": "Judge",
            "current_aggressive_response": risk_debate_state["current_aggressive_response"],
            "current_conservative_response": risk_debate_state["current_conservative_response"],
            "current_neutral_response": risk_debate_state["current_neutral_response"],
            "count": risk_debate_state["count"],
        }

        return {
            "risk_debate_state": new_risk_debate_state,
            "final_trade_decision": final_trade_decision,
        }

    return portfolio_manager_node
