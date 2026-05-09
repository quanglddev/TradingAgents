"""Quorum-mode per-agent model routing.

This module is the single source of truth for the ``tradingagents-quorum``
entry point. Instead of running every agent on a single vendor (the default
behavior in ``TradingAgentsGraph``), each agent is mapped to the frontier
model that best fits its role while keeping total cost down. Routing is
informed by the public Artificial Analysis Intelligence Index v4.0
(intelligence + price + speed) and the per-agent prompts in
``tradingagents/agents/``.

Allowed deep-thinker models, per the user's brief:

- OpenAI ``gpt-5.4`` with ``reasoning_effort="xhigh"`` (the actual OpenAI
  API value above ``high``; verified accepted on GPT-5.4 / GPT-5.5).
  langchain-openai forwards the string verbatim even though its public
  type-hint enumerates only ``low/medium/high``.
- Anthropic ``claude-opus-4-6`` with ``effort="high"`` (the maximum that
  the Anthropic API exposes; "max" on Artificial Analysis is their own
  label, not an additional API tier).
- DeepSeek ``deepseek-v4-pro`` (the V4 flagship; built-in thinking, no
  separate effort dial).

A single cheap "quick" model (``deepseek-v4-flash``) is reserved for the
Reflector — a 2-4 sentence post-mortem that runs at the start of the
*next* same-ticker run and does not benefit from a frontier model.

Why these picks (cost & quality pareto, AA Intelligence Index v4.0):

- DeepSeek V4 Pro Max — Intelligence 52, $2.2 / 1M tokens. ~5x cheaper
  than GPT-5.4 (xhigh) at $5.6 / 1M and Claude Opus 4.6 max at
  $10.9 / 1M. Used as the workhorse for high-frequency debate seats
  (Bull, Aggressive, Neutral) and language-heavy analyst seats (Market,
  Social, News) where its quality is sufficient.
- GPT-5.4 (xhigh) — Intelligence 57, $5.6 / 1M, 1M context. Strongest
  numeric / coding chain. Used for Fundamentals (financial-statement
  math) and the precision-debate seats (Bear, Conservative). Also used
  for the Trader's structured proposal because OpenAI's function-calling
  path is the most reliable.
- Claude Opus 4.6 (max) — Intelligence 57, $10.9 / 1M. Reserved for the
  two single-call synthesis-and-judge nodes (Research Manager,
  Portfolio Manager) where the quality premium is highest and the call
  count is lowest.

If you change this map, also update the docstring above so the rationale
stays linked to the routing.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Tuple

from tradingagents.llm_clients import create_llm_client


# (provider, model, llm-kwargs)
ProviderRoute = Tuple[str, str, Dict[str, Any]]


# Per-agent routing. Keys must match the agent names used by
# ``GraphSetup._llm_for`` exactly: see ``tradingagents/graph/setup.py``.
QUORUM_ROUTING: Dict[str, ProviderRoute] = {
    # --- Analyst Team (each calls tools then writes one final report) ---
    "Market Analyst":       ("deepseek",  "deepseek-v4-pro", {}),
    "Social Analyst":       ("deepseek",  "deepseek-v4-pro", {}),
    "News Analyst":         ("deepseek",  "deepseek-v4-pro", {}),
    "Fundamentals Analyst": ("openai",    "gpt-5.4",         {"reasoning_effort": "xhigh"}),

    # --- Research debate (5 rounds × 2 = 10 turns at deep depth) ---
    "Bull Researcher":      ("deepseek",  "deepseek-v4-pro", {}),
    "Bear Researcher":      ("openai",    "gpt-5.4",         {"reasoning_effort": "xhigh"}),
    # Single judge call — premium model worth the cost here.
    "Research Manager":     ("anthropic", "claude-opus-4-6", {"effort": "high"}),

    # --- Trader (single structured-output call) ---
    "Trader":               ("openai",    "gpt-5.4",         {"reasoning_effort": "xhigh"}),

    # --- Risk panel (5 rounds × 3 = 15 turns at deep depth) ---
    "Aggressive Analyst":   ("deepseek",  "deepseek-v4-pro", {}),
    "Conservative Analyst": ("openai",    "gpt-5.4",         {"reasoning_effort": "xhigh"}),
    "Neutral Analyst":      ("deepseek",  "deepseek-v4-pro", {}),

    # --- Final decision (single call) ---
    "Portfolio Manager":    ("anthropic", "claude-opus-4-6", {"effort": "high"}),
}


# Reflector is a once-per-run, 2-4 sentence post-mortem that runs at the
# start of the NEXT same-ticker run. Frontier models are wasted here.
REFLECTOR_ROUTE: ProviderRoute = ("deepseek", "deepseek-v4-flash", {})


# Vendors that the quorum routing actually exercises. Keep this in sync
# with QUORUM_ROUTING / REFLECTOR_ROUTE so the env-key check fails fast
# with an actionable message rather than partway into an analyst loop.
_REQUIRED_ENV_KEYS: Dict[str, str] = {
    "openai":    "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "deepseek":  "DEEPSEEK_API_KEY",
}


def required_providers() -> List[str]:
    """Return the lower-case provider names referenced by the routing."""
    providers = {p for p, _, _ in QUORUM_ROUTING.values()}
    providers.add(REFLECTOR_ROUTE[0])
    return sorted(providers)


def missing_api_keys() -> List[str]:
    """Return env-var names that are required but not populated.

    Used by the ``quorum`` CLI entry point to fail fast with a single
    clear error rather than producing a partial run that crashes mid-way
    through when the first call to a missing-key provider lands.
    """
    missing: List[str] = []
    for provider in required_providers():
        env_var = _REQUIRED_ENV_KEYS.get(provider)
        if env_var and not os.environ.get(env_var):
            missing.append(env_var)
    return missing


def _build_llm(
    provider: str,
    model: str,
    kwargs: Dict[str, Any],
    callbacks: Optional[List[Any]],
) -> Any:
    """Construct a single LLM with provider-specific kwargs and optional callbacks.

    Callbacks are forwarded through every per-agent client so the
    StatsCallbackHandler in the CLI sees every LLM call regardless of
    which vendor served it.
    """
    extra = dict(kwargs)
    if callbacks:
        extra["callbacks"] = callbacks
    client = create_llm_client(provider=provider, model=model, **extra)
    return client.get_llm()


def build_quorum_llm_map(
    callbacks: Optional[List[Any]] = None,
) -> Dict[str, Any]:
    """Build one ready-to-use LLM per agent, sharing instances when possible.

    Two agents pinned to the same (provider, model, kwargs) tuple share a
    single underlying LLM object. This keeps connection pools small and
    lets stats callbacks aggregate calls naturally. The mapping returned
    is consumed by ``GraphSetup`` via the ``agent_llm_map`` argument.
    """
    cache: Dict[Tuple[str, str, frozenset], Any] = {}
    llm_map: Dict[str, Any] = {}
    for agent_name, (provider, model, kwargs) in QUORUM_ROUTING.items():
        cache_key = (provider, model, frozenset(kwargs.items()))
        if cache_key not in cache:
            cache[cache_key] = _build_llm(provider, model, kwargs, callbacks)
        llm_map[agent_name] = cache[cache_key]
    return llm_map


def build_reflector_llm(callbacks: Optional[List[Any]] = None) -> Any:
    """Construct the cheap quick-think LLM used by Reflector / fallbacks."""
    provider, model, kwargs = REFLECTOR_ROUTE
    return _build_llm(provider, model, kwargs, callbacks)


def describe_routing() -> str:
    """Human-readable summary printed by the CLI before a run.

    Helps the user verify the multi-vendor routing is what they expect
    when staring at a Live console panel.
    """
    rows = []
    for agent, (provider, model, kwargs) in QUORUM_ROUTING.items():
        kwargs_str = (
            ", ".join(f"{k}={v}" for k, v in kwargs.items()) or "default"
        )
        rows.append(f"  - {agent:<22s} → {provider}:{model} ({kwargs_str})")
    rprov, rmodel, _ = REFLECTOR_ROUTE
    rows.append(f"  - {'Reflector (post-mortem)':<22s} → {rprov}:{rmodel}")
    return "\n".join(rows)
