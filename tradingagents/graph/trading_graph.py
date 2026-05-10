# TradingAgents/graph/trading_graph.py

import logging
import os
from contextlib import contextmanager
from pathlib import Path
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Iterator, Tuple, List, Optional

import yfinance as yf

logger = logging.getLogger(__name__)

from langgraph.prebuilt import ToolNode

from tradingagents.llm_clients import create_llm_client

from tradingagents.agents import *
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.agents.utils.memory import TradingMemoryLog
from tradingagents.dataflows.utils import safe_ticker_component
from tradingagents.agents.utils.agent_states import (
    AgentState,
    InvestDebateState,
    RiskDebateState,
)
from tradingagents.dataflows.config import set_config

# Import the new abstract tool methods from agent_utils
from tradingagents.agents.utils.agent_utils import (
    get_stock_data,
    get_indicators,
    get_fundamentals,
    get_balance_sheet,
    get_cashflow,
    get_income_statement,
    get_news,
    get_insider_transactions,
    get_global_news
)

from .checkpointer import (
    checkpoint_step,
    clear_checkpoint,
    get_checkpointer,
    has_checkpoint,
    thread_id,
)
from .conditional_logic import ConditionalLogic
from .setup import GraphSetup
from .propagation import Propagator
from .reflection import Reflector
from .signal_processing import SignalProcessor


class TradingAgentsGraph:
    """Main class that orchestrates the trading agents framework."""

    def __init__(
        self,
        selected_analysts=["market", "social", "news", "fundamentals"],
        debug=False,
        config: Dict[str, Any] = None,
        callbacks: Optional[List] = None,
        agent_llm_map: Optional[Dict[str, Any]] = None,
        reflector_llm: Optional[Any] = None,
    ):
        """Initialize the trading agents graph and components.

        Args:
            selected_analysts: List of analyst types to include
            debug: Whether to run in debug mode
            config: Configuration dictionary. If None, uses default config
            callbacks: Optional list of callback handlers (e.g., for tracking LLM/tool stats)
            agent_llm_map: Optional pre-built ``{agent_name: llm}`` map.
                When provided, the per-agent LLMs in ``GraphSetup``
                bypass the single-vendor deep/quick split. Used by the
                ``tradingagents-quorum`` CLI to route each agent to its
                own best-fit frontier model. Unmapped agents fall back
                to ``thinking_policy`` selection.
            reflector_llm: Optional pre-built LLM for the post-mortem
                Reflector. When provided, it overrides the default
                ``quick_thinking_llm``. The Reflector runs at the start
                of the *next* same-ticker run, so a cheap model is
                appropriate even in quorum mode.
        """
        self.debug = debug
        self.config = config or DEFAULT_CONFIG
        self.callbacks = callbacks or []

        # Update the interface's config
        set_config(self.config)

        # Create necessary directories
        os.makedirs(self.config["data_cache_dir"], exist_ok=True)
        os.makedirs(self.config["results_dir"], exist_ok=True)

        if agent_llm_map:
            # Quorum mode: each agent gets its own LLM. We still need
            # ``deep_thinking_llm`` and ``quick_thinking_llm`` populated
            # for any agents not in the map and for SignalProcessor's
            # backwards-compatible constructor argument.
            map_values = list(agent_llm_map.values())
            fallback = (
                agent_llm_map.get("Research Manager")
                or agent_llm_map.get("Portfolio Manager")
                or map_values[0]
            )
            self.deep_thinking_llm = fallback
            self.quick_thinking_llm = reflector_llm or fallback
        else:
            llm_kwargs = self._get_provider_kwargs()
            if self.callbacks:
                llm_kwargs["callbacks"] = self.callbacks

            deep_client = create_llm_client(
                provider=self.config["llm_provider"],
                model=self.config["deep_think_llm"],
                base_url=self.config.get("backend_url"),
                **llm_kwargs,
            )
            quick_client = create_llm_client(
                provider=self.config["llm_provider"],
                model=self.config["quick_think_llm"],
                base_url=self.config.get("backend_url"),
                **llm_kwargs,
            )

            self.deep_thinking_llm = deep_client.get_llm()
            self.quick_thinking_llm = quick_client.get_llm()

        self.memory_log = TradingMemoryLog(self.config)

        # Create tool nodes
        self.tool_nodes = self._create_tool_nodes()

        # Initialize components
        self.conditional_logic = ConditionalLogic(
            max_debate_rounds=self.config["max_debate_rounds"],
            max_risk_discuss_rounds=self.config["max_risk_discuss_rounds"],
        )
        self.graph_setup = GraphSetup(
            self.quick_thinking_llm,
            self.deep_thinking_llm,
            self.tool_nodes,
            self.conditional_logic,
            config=self.config,
            agent_llm_map=agent_llm_map,
        )

        self.propagator = Propagator()
        self.reflector = Reflector(self.quick_thinking_llm)
        self.signal_processor = SignalProcessor(self.quick_thinking_llm)

        # State tracking
        self.curr_state = None
        self.ticker = None
        self.log_states_dict = {}  # date to full state dict

        # Set up the graph: keep the workflow for recompilation with a checkpointer.
        self.workflow = self.graph_setup.setup_graph(selected_analysts)
        self.graph = self.workflow.compile()
        self._checkpointer_ctx = None

    def _get_provider_kwargs(self) -> Dict[str, Any]:
        """Get provider-specific kwargs for LLM client creation."""
        kwargs = {}
        provider = self.config.get("llm_provider", "").lower()

        if provider == "google":
            thinking_level = self.config.get("google_thinking_level")
            if thinking_level:
                kwargs["thinking_level"] = thinking_level

        elif provider == "openai":
            reasoning_effort = self.config.get("openai_reasoning_effort")
            if reasoning_effort:
                kwargs["reasoning_effort"] = reasoning_effort

        elif provider == "anthropic":
            effort = self.config.get("anthropic_effort")
            if effort:
                kwargs["effort"] = effort

        return kwargs

    def _create_tool_nodes(self) -> Dict[str, ToolNode]:
        """Create tool nodes for different data sources using abstract methods."""
        return {
            "market": ToolNode(
                [
                    # Core stock data tools
                    get_stock_data,
                    # Technical indicators
                    get_indicators,
                ]
            ),
            "social": ToolNode(
                [
                    # News tools for social media analysis
                    get_news,
                ]
            ),
            "news": ToolNode(
                [
                    # News and insider information
                    get_news,
                    get_global_news,
                    get_insider_transactions,
                ]
            ),
            "fundamentals": ToolNode(
                [
                    # Fundamental analysis tools
                    get_fundamentals,
                    get_balance_sheet,
                    get_cashflow,
                    get_income_statement,
                ]
            ),
        }

    def _fetch_returns(
        self, ticker: str, trade_date: str, holding_days: int = 5
    ) -> Tuple[Optional[float], Optional[float], Optional[int]]:
        """Fetch raw and alpha return for ticker over holding_days from trade_date.

        Returns (raw_return, alpha_return, actual_holding_days) or
        (None, None, None) if price data is unavailable (too recent, delisted,
        or network error).
        """
        try:
            start = datetime.strptime(trade_date, "%Y-%m-%d")
            end = start + timedelta(days=holding_days + 7)  # buffer for weekends/holidays
            end_str = end.strftime("%Y-%m-%d")

            stock = yf.Ticker(ticker).history(start=trade_date, end=end_str)
            spy = yf.Ticker("SPY").history(start=trade_date, end=end_str)

            if len(stock) < 2 or len(spy) < 2:
                return None, None, None

            actual_days = min(holding_days, len(stock) - 1, len(spy) - 1)
            raw = float(
                (stock["Close"].iloc[actual_days] - stock["Close"].iloc[0])
                / stock["Close"].iloc[0]
            )
            spy_ret = float(
                (spy["Close"].iloc[actual_days] - spy["Close"].iloc[0])
                / spy["Close"].iloc[0]
            )
            alpha = raw - spy_ret
            return raw, alpha, actual_days
        except Exception as e:
            logger.warning(
                "Could not resolve outcome for %s on %s (will retry next run): %s",
                ticker, trade_date, e,
            )
            return None, None, None

    # --- Public hooks for entry points that drive the graph manually ---

    def has_pending_checkpoint(self, ticker: str, trade_date) -> bool:
        """Return True if a resumable checkpoint exists for this run.

        Wraps :func:`tradingagents.graph.checkpointer.has_checkpoint`
        so callers (CLI surfaces, dashboards) don't need to import the
        low-level module or know the cache directory layout. Returns
        False when checkpointing is disabled or no prior crash left a
        checkpoint behind.
        """
        if not self.config.get("checkpoint_enabled"):
            return False
        return has_checkpoint(
            self.config["data_cache_dir"], ticker, str(trade_date)
        )

    @contextmanager
    def checkpointed_run(
        self, ticker: str, trade_date
    ) -> Iterator[Optional[str]]:
        """Compile the graph against a per-ticker SqliteSaver for the
        duration of the context, then restore the plain compilation on
        exit.

        Yields the LangGraph ``thread_id`` for this run when
        ``checkpoint_enabled`` is True, or ``None`` when checkpointing
        is disabled (in which case this context manager is a pass-
        through). Callers must inject the yielded thread_id into the
        ``args`` they pass to :meth:`graph.stream`/:meth:`graph.invoke`
        so LangGraph routes state to the right thread::

            with graph.checkpointed_run(ticker, date) as tid:
                if tid is not None:
                    args.setdefault("config", {}) \\
                        .setdefault("configurable", {})["thread_id"] = tid
                final_state = graph.graph.invoke(state, **args)
                graph.clear_checkpoint_for(ticker, date)  # only on success

        On a clean exit the per-run checkpoint is intentionally NOT
        cleared here — that is the caller's responsibility via
        :meth:`clear_checkpoint_for` so a crashed mid-run leaves the
        checkpoint behind for resume.
        """
        if not self.config.get("checkpoint_enabled"):
            yield None
            return

        ctx = get_checkpointer(self.config["data_cache_dir"], ticker)
        saver = ctx.__enter__()
        self.graph = self.workflow.compile(checkpointer=saver)
        self._checkpointer_ctx = ctx
        try:
            step = checkpoint_step(
                self.config["data_cache_dir"], ticker, str(trade_date)
            )
            if step is not None:
                logger.info(
                    "Resuming from step %d for %s on %s",
                    step, ticker, trade_date,
                )
            else:
                logger.info(
                    "Starting fresh for %s on %s", ticker, trade_date
                )
            yield thread_id(ticker, str(trade_date))
        finally:
            ctx.__exit__(None, None, None)
            self._checkpointer_ctx = None
            self.graph = self.workflow.compile()

    def clear_checkpoint_for(self, ticker: str, trade_date) -> None:
        """Drop the resume-checkpoint for ``(ticker, trade_date)``.

        Idempotent and a no-op when ``checkpoint_enabled`` is False.
        Call after a run completes successfully so a future re-run for
        the same date starts fresh; skipping it on failure preserves
        the checkpoint so the next invocation can resume.
        """
        if not self.config.get("checkpoint_enabled"):
            return
        clear_checkpoint(
            self.config["data_cache_dir"], ticker, str(trade_date)
        )

    def prepare_memory_context(self, ticker: str) -> str:
        """Resolve outstanding reflections for ``ticker`` and return the
        formatted past_context string for Portfolio Manager injection.

        ``propagate()`` calls this internally. CLI entry points that
        stream the LangGraph workflow themselves (e.g.
        ``execute_with_live_display`` shared by ``tradingagents analyze``
        and ``tradingagents-quorum``) call this directly so the same
        cross-run memory that the Python API exposes is also active in
        the interactive flows. Returns ``""`` when no prior context
        exists or the memory log is disabled.
        """
        self._resolve_pending_entries(ticker)
        return self.memory_log.get_past_context(ticker)

    def record_decision(
        self,
        ticker: str,
        trade_date,
        final_state,
    ) -> None:
        """Persist a completed run's final decision to the memory log.

        No-op when ``final_state`` lacks ``final_trade_decision`` (e.g.
        a run interrupted before the Portfolio Manager produced output)
        or when the memory log path is unset. ``store_decision`` itself
        is idempotent over (ticker, trade_date), so repeated calls in
        the same calendar day collapse to a single pending entry.
        """
        if not isinstance(final_state, dict):
            return
        decision = final_state.get("final_trade_decision")
        if not decision:
            return
        self.memory_log.store_decision(
            ticker=ticker,
            trade_date=str(trade_date),
            final_trade_decision=decision,
        )

    def _resolve_pending_entries(self, ticker: str) -> None:
        """Resolve pending log entries for ticker at the start of a new run.

        Fetches returns for each same-ticker pending entry, generates reflections,
        then writes all updates in a single atomic batch write to avoid redundant I/O.
        Skips entries whose price data is not yet available (too recent or delisted).

        Trade-off: only same-ticker entries are resolved per run.  Entries for
        other tickers accumulate until that ticker is run again.
        """
        pending = [e for e in self.memory_log.get_pending_entries() if e["ticker"] == ticker]
        if not pending:
            return

        updates = []
        for entry in pending:
            raw, alpha, days = self._fetch_returns(ticker, entry["date"])
            if raw is None:
                continue  # price not available yet — try again next run
            reflection = self.reflector.reflect_on_final_decision(
                final_decision=entry.get("decision", ""),
                raw_return=raw,
                alpha_return=alpha,
            )
            updates.append({
                "ticker": ticker,
                "trade_date": entry["date"],
                "raw_return": raw,
                "alpha_return": alpha,
                "holding_days": days,
                "reflection": reflection,
            })

        if updates:
            self.memory_log.batch_update_with_outcomes(updates)

    def propagate(self, company_name, trade_date):
        """Run the trading agents graph for a company on a specific date.

        When ``checkpoint_enabled`` is set in config, the graph is recompiled
        with a per-ticker SqliteSaver so a crashed run can resume from the last
        successful node on a subsequent invocation with the same ticker+date.
        """
        self.ticker = company_name

        # Resolve any pending memory-log entries for this ticker before the pipeline runs.
        self._resolve_pending_entries(company_name)

        # Compile-with-checkpointer / restore lifecycle is handled by the
        # context manager. Thread-id injection into args still happens
        # inside ``_run_graph`` (it re-derives the same id via thread_id()),
        # so we don't need the yielded value here.
        with self.checkpointed_run(company_name, trade_date):
            return self._run_graph(company_name, trade_date)

    def _run_graph(self, company_name, trade_date):
        """Execute the graph and write the resulting state to disk and memory log."""
        # Initialize state — inject memory log context for PM.
        past_context = self.memory_log.get_past_context(company_name)
        init_agent_state = self.propagator.create_initial_state(
            company_name, trade_date, past_context=past_context
        )
        args = self.propagator.get_graph_args()

        # Inject thread_id so same ticker+date resumes, different date starts fresh.
        if self.config.get("checkpoint_enabled"):
            tid = thread_id(company_name, str(trade_date))
            args.setdefault("config", {}).setdefault("configurable", {})["thread_id"] = tid

        if self.debug:
            trace = []
            for chunk in self.graph.stream(init_agent_state, **args):
                if len(chunk["messages"]) == 0:
                    pass
                else:
                    chunk["messages"][-1].pretty_print()
                    trace.append(chunk)
            final_state = trace[-1]
        else:
            final_state = self.graph.invoke(init_agent_state, **args)

        # Store current state for reflection.
        self.curr_state = final_state

        # Log state to disk.
        self._log_state(trade_date, final_state)

        # Store decision for deferred reflection on the next same-ticker run.
        self.memory_log.store_decision(
            ticker=company_name,
            trade_date=trade_date,
            final_trade_decision=final_state["final_trade_decision"],
        )

        # Clear checkpoint on successful completion to avoid stale state.
        if self.config.get("checkpoint_enabled"):
            clear_checkpoint(
                self.config["data_cache_dir"], company_name, str(trade_date)
            )

        return final_state, self.process_signal(final_state["final_trade_decision"])

    def _log_state(self, trade_date, final_state):
        """Log the final state to a JSON file."""
        self.log_states_dict[str(trade_date)] = {
            "company_of_interest": final_state["company_of_interest"],
            "trade_date": final_state["trade_date"],
            "market_report": final_state["market_report"],
            "sentiment_report": final_state["sentiment_report"],
            "news_report": final_state["news_report"],
            "fundamentals_report": final_state["fundamentals_report"],
            "investment_debate_state": {
                "bull_history": final_state["investment_debate_state"]["bull_history"],
                "bear_history": final_state["investment_debate_state"]["bear_history"],
                "history": final_state["investment_debate_state"]["history"],
                "current_response": final_state["investment_debate_state"][
                    "current_response"
                ],
                "judge_decision": final_state["investment_debate_state"][
                    "judge_decision"
                ],
            },
            "trader_investment_decision": final_state["trader_investment_plan"],
            "risk_debate_state": {
                "aggressive_history": final_state["risk_debate_state"]["aggressive_history"],
                "conservative_history": final_state["risk_debate_state"]["conservative_history"],
                "neutral_history": final_state["risk_debate_state"]["neutral_history"],
                "history": final_state["risk_debate_state"]["history"],
                "judge_decision": final_state["risk_debate_state"]["judge_decision"],
            },
            "investment_plan": final_state["investment_plan"],
            "final_trade_decision": final_state["final_trade_decision"],
        }

        # Save to file. Reject ticker values that would escape the
        # results directory when joined as a path component.
        safe_ticker = safe_ticker_component(self.ticker)
        directory = Path(self.config["results_dir"]) / safe_ticker / "TradingAgentsStrategy_logs"
        directory.mkdir(parents=True, exist_ok=True)

        log_path = directory / f"full_states_log_{trade_date}.json"
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(self.log_states_dict[str(trade_date)], f, indent=4)

    def process_signal(self, full_signal):
        """Process a signal to extract the core decision."""
        return self.signal_processor.process_signal(full_signal)
