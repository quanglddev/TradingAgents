"""Research Manager: turns the bull/bear debate into a structured investment plan for the trader."""

from __future__ import annotations

from tradingagents.agents.schemas import ResearchPlan, render_research_plan
from tradingagents.agents.utils.agent_utils import (
    append_style_instruction,
    build_instrument_context,
)
from tradingagents.agents.utils.structured import (
    bind_structured,
    invoke_structured_or_freetext,
)


def create_research_manager(llm):
    structured_llm = bind_structured(llm, ResearchPlan, "Research Manager")

    def research_manager_node(state) -> dict:
        instrument_context = build_instrument_context(state["company_of_interest"])
        history = state["investment_debate_state"].get("history", "")

        investment_debate_state = state["investment_debate_state"]

        prompt = f"""You are the Research Manager. Arbitrate the bull/bear debate and produce ONE decisive investment plan the Trader can execute. You judge the debate; you do not transcribe it.

<context>
{instrument_context}
</context>

<rating_scale>
Pick exactly ONE. Definitions are strict.
- **Buy**: Bull case clearly dominates; multiple independent confirmations; identifiable near-term catalyst. Recommend opening or topping up to full target weight.
- **Overweight**: Bull case wins on net but residual bear risk unresolved. Recommend gradual accumulation, partial size, leave room to add on confirmation.
- **Hold**: Genuinely balanced — bull and bear arguments offset on materially equal evidence weight. Use ONLY when neither side dominates AND no catalyst is imminent. Never use Hold to dodge a call.
- **Underweight**: Bear case wins on net but a residual bullish tailwind exists. Recommend trimming or running below benchmark; keep a starter only if asymmetric upside catalyst remains.
- **Sell**: Bear case clearly dominates; thesis-breaking risk active or capital better deployed elsewhere. Recommend full exit / avoid.
</rating_scale>

<rubric>
1. Score, do not summarize. For each major claim from each side, weight = (evidence quality) × (recency) × (independence). Discount: anecdotes, cherry-picked windows, narrative-only points, claims contradicted by data already cited in the debate.
2. Tie-break ladder (apply IN ORDER, stop at the first that resolves):
   a. Which side has cleaner falsifiable evidence?
   b. Which side has asymmetric payoff (bounded downside vs open upside, or vice versa)?
   c. Which side aligns with the historical or sector base rate?
   d. Only if a/b/c are all truly equal → Hold.
3. Decisiveness: if step 2 resolves at a/b/c, you MUST commit. Hold is a real verdict, not an escape from indecision.
4. Strategic actions must be operational: time horizon, sizing posture (e.g. "build to 1/3 of target over 5 sessions, scale on confirmation"), risk caps, the catalyst window the position is held into.
</rubric>

<evidence_discipline>
- Cite only facts surfaced in the debate history or instrument context above. No invented prices, multiples, dates, percentages, analyst targets, or earnings figures.
- If a critical figure is missing, name it as a known unknown and state how it would update the rating.
- Distinguish FACT (in transcript) from INFERENCE (your synthesis). Do not blur.
</evidence_discipline>

<calibration>
Inside your rationale, state explicitly:
- Conviction label: Low / Med / High.
- One UPGRADE flip-condition: a specific observable that would force a one-tier upgrade.
- One DOWNGRADE flip-condition: a specific observable that would force a one-tier downgrade.
A plan without both flip-conditions is incomplete.
</calibration>

<anti_patterns>
- No "this is a complex situation", no "on balance" without showing the ladder above.
- No restating both sides at equal length and then declining to verdict.
- No thesis without an explicit invalidation condition.
- No generic actions ("monitor closely", "stay disciplined", "watch for developments").
</anti_patterns>

<debate_history>
{history}
</debate_history>

<output_contract>
Fill the structured schema. Be terse and specific inside each field; substance over volume.
If your runtime forces free-text output, you MUST start the response with `**Rating**: X` (X ∈ {{Buy, Overweight, Hold, Underweight, Sell}}) on the first line, so downstream parsers (signal processor, memory log) keep working. The prose that follows must still satisfy the rubric above.
</output_contract>"""
        prompt = append_style_instruction(prompt)

        investment_plan = invoke_structured_or_freetext(
            structured_llm,
            llm,
            prompt,
            render_research_plan,
            "Research Manager",
        )

        new_investment_debate_state = {
            "judge_decision": investment_plan,
            "history": investment_debate_state.get("history", ""),
            "bear_history": investment_debate_state.get("bear_history", ""),
            "bull_history": investment_debate_state.get("bull_history", ""),
            "current_response": investment_plan,
            "count": investment_debate_state["count"],
        }

        return {
            "investment_debate_state": new_investment_debate_state,
            "investment_plan": investment_plan,
        }

    return research_manager_node
