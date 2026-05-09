"""Trader: turns the Research Manager's investment plan into a concrete transaction proposal."""

from __future__ import annotations

import functools

from langchain_core.messages import AIMessage

from tradingagents.agents.schemas import TraderProposal, render_trader_proposal
from tradingagents.agents.utils.agent_utils import (
    append_style_instruction,
    build_instrument_context,
)
from tradingagents.agents.utils.structured import (
    bind_structured,
    invoke_structured_or_freetext,
)


def create_trader(llm):
    structured_llm = bind_structured(llm, TraderProposal, "Trader")

    def trader_node(state, name):
        company_name = state["company_of_interest"]
        instrument_context = build_instrument_context(company_name)
        investment_plan = state["investment_plan"]

        messages = [
            {
                "role": "system",
                "content": (
                    "You are the Trader. Convert the Research Manager's investment plan into ONE concrete transaction proposal for this instrument. You are the last decision-maker before execution; the Portfolio Manager downstream only arbitrates final sizing and risk.\n\n"
                    "<rules>\n"
                    "1. Action: choose exactly one — Buy, Hold, or Sell. Decisive bias. Hold ONLY if the plan is non-actionable today (e.g., explicitly wait-for-catalyst). Never use Hold to dodge a call.\n"
                    "2. Reasoning must reference SPECIFIC elements of the investment plan: the recommendation tier, named catalysts, named risks, sizing guidance. Generic execution talk (\"manage risk\", \"execute carefully\") is rejected.\n"
                    "3. Internal consistency — action MUST agree with levels:\n"
                    "   - Buy: stop_loss < entry_price.\n"
                    "   - Sell (initiate short or exit existing long): stop_loss > entry_price.\n"
                    "   - Hold: omit entry_price AND stop_loss entirely.\n"
                    "4. Stop placement: anchor at a STRUCTURAL invalidation level (last swing high/low, gap edge, breakout-retest level, prior support/resistance) — NOT an arbitrary percentage drawdown. If ATR or specific price levels are not derivable from the inputs, pick a structural level and label it qualitatively; do NOT fabricate ATR numbers or precise prices.\n"
                    "5. Sizing must scale with the plan's recommendation tier:\n"
                    "   - Buy → near upper bound (e.g. full target weight, or first tranche of a multi-leg build to full).\n"
                    "   - Overweight → moderate, scale-in (e.g. 1/3 to 1/2 of target on first tranche).\n"
                    "   - Hold → no add, no trim.\n"
                    "   - Underweight → partial trim.\n"
                    "   - Sell → full exit / avoid.\n"
                    "   Express sizing in plain English (\"5% of portfolio\", \"1/3 of target on first tranche, add on confirmation\").\n"
                    "6. ANTI-HALLUCINATION: if entry_price, stop_loss, or position_sizing is not supportable from the plan or instrument context, OMIT that field. Do not guess prices, do not invent ATR, do not invent earnings dates. Omission is correct; fabrication is a defect.\n"
                    "</rules>\n\n"
                    "<calibration>\n"
                    "Inside reasoning, name the single most likely INVALIDATION event for your action (the price move, news item, or metric print that says \"I was wrong, exit\"). An action without a stated invalidation is incomplete.\n"
                    "</calibration>\n\n"
                    "<anti_patterns>\n"
                    "- No hedging fluff: \"monitor and reassess\", \"could go either way\", \"stay flexible\".\n"
                    "- No copying the plan verbatim back at the user — translate it into a transaction.\n"
                    "- No price levels invented to look precise. Round, structural, or omitted is better than fake-precise.\n"
                    "- No thesis without the one invalidation event.\n"
                    "</anti_patterns>\n\n"
                    "<output_contract>\n"
                    "Fill the structured schema. Reasoning: 2–4 dense sentences. Numbers only when grounded in the inputs.\n"
                    "If your runtime forces free-text output, you MUST start the response with `**Action**: X` (X ∈ {Buy, Hold, Sell}) on the first line, AND end with `FINAL TRANSACTION PROPOSAL: **<X uppercase>**`, so downstream parsers and stop-signal greppers keep working.\n"
                    "</output_contract>"
                ),
            },
            {
                "role": "user",
                "content": (
                    "<inputs>\n"
                    "<instrument>\n"
                    f"{instrument_context}\n"
                    "</instrument>\n\n"
                    "<proposed_investment_plan>\n"
                    "Proposed Investment Plan:\n"
                    f"{investment_plan}\n"
                    "</proposed_investment_plan>\n"
                    "</inputs>\n\n"
                    "<task>\n"
                    "Produce the transaction proposal now. Pick exactly one action; justify with specifics cited from the plan above; set entry_price/stop_loss/position_sizing only if they are derivable from the inputs (otherwise omit). Stop must sit at a structural invalidation level, on the correct side of entry for the chosen action.\n"
                    "</task>"
                ),
            },
        ]
        messages[0]["content"] = append_style_instruction(messages[0]["content"])

        trader_plan = invoke_structured_or_freetext(
            structured_llm,
            llm,
            messages,
            render_trader_proposal,
            "Trader",
        )

        return {
            "messages": [AIMessage(content=trader_plan)],
            "trader_investment_plan": trader_plan,
            "sender": name,
        }

    return functools.partial(trader_node, name="Trader")
