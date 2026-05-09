"""``tradingagents-quorum`` — multi-vendor, ticker-only entry point.

This script is the "extreme-optimized" default: pass a ticker, get a full
trading analysis where every agent runs on the frontier model best suited
to its role (across OpenAI, Anthropic, and DeepSeek). All other knobs
(date, language, prompt style, analyst team, research depth) are pinned
to opinionated defaults rather than asked interactively. The legacy
``tradingagents analyze`` command (with ``--checkpoint`` and full
interactive setup) is preserved unchanged.

Usage::

    tradingagents-quorum AAPL                 # today, English, caveman, all 4 analysts, deep
    tradingagents-quorum AAPL --date 2026-05-08
    tradingagents-quorum AAPL --no-save       # skip writing reports/<TICKER>_<TS>/

API keys for OpenAI, Anthropic, and DeepSeek must all be present in
``.env`` (or the environment) before invocation. The script fails fast
with an explicit list of missing keys instead of partial-running.
"""

from __future__ import annotations

import datetime as _dt
import logging
import os
import sys
import time
from pathlib import Path
from typing import List, Optional

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule

# Load .env BEFORE importing the graph (which reads provider env vars at
# client construction time). ``override=False`` so process-level vars win.
load_dotenv()
load_dotenv(".env.enterprise", override=False)

# Reuse the report writer / display from the interactive CLI so the
# on-disk layout stays consistent across both entry points.
from cli.main import display_complete_report, save_report_to_disk
from cli.stats_handler import StatsCallbackHandler
from tradingagents.agent_model_routing import (
    build_quorum_llm_map,
    build_reflector_llm,
    describe_routing,
    missing_api_keys,
)
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph.trading_graph import TradingAgentsGraph


console = Console()
logger = logging.getLogger("tradingagents.quorum")


app = typer.Typer(
    name="tradingagents-quorum",
    help=(
        "Run a TradingAgents analysis with the per-agent best-fit model "
        "routing across OpenAI / Anthropic / DeepSeek. Defaults: today, "
        "English, caveman prose, all 4 analysts, deep research depth."
    ),
    add_completion=True,
)


# Default selections baked into quorum mode. These are deliberately not
# CLI flags — the whole point of this entry point is "give me the best
# possible report from a single ticker".
_DEFAULT_ANALYSTS: List[str] = ["market", "social", "news", "fundamentals"]
_DEFAULT_RESEARCH_DEPTH: int = 5         # "Deep" preset in interactive CLI
_DEFAULT_PROMPT_STYLE: str = "caveman"   # token-efficient, low-filler prose
_DEFAULT_OUTPUT_LANGUAGE: str = "English"


def _validate_ticker(ticker: str) -> str:
    """Normalize and minimally validate a ticker string.

    Mirrors ``cli/utils.normalize_ticker_symbol`` — strip + uppercase,
    preserving any exchange suffix (``.TO``, ``.HK``, ``.T``, ``.L``).
    """
    cleaned = (ticker or "").strip().upper()
    if not cleaned:
        raise typer.BadParameter("Ticker cannot be empty.")
    return cleaned


def _validate_date(date_str: Optional[str]) -> str:
    """Return a valid YYYY-MM-DD; default to today, reject future dates."""
    today = _dt.date.today()
    if not date_str:
        return today.strftime("%Y-%m-%d")
    try:
        parsed = _dt.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as exc:
        raise typer.BadParameter(
            f"Invalid date '{date_str}'. Use YYYY-MM-DD."
        ) from exc
    if parsed > today:
        raise typer.BadParameter(
            f"Analysis date {date_str} is in the future."
        )
    return parsed.strftime("%Y-%m-%d")


def _abort_if_keys_missing() -> None:
    """Stop early when any of the three required vendor keys are unset.

    Catching this here avoids an obscure failure halfway through an
    analyst loop when the first call to a missing-key vendor lands.
    """
    missing = missing_api_keys()
    if not missing:
        return
    console.print(
        Panel(
            "Quorum mode routes agents across OpenAI, Anthropic, and "
            "DeepSeek. The following API keys are missing from your "
            "environment / .env file:\n\n"
            + "\n".join(f"  - {k}" for k in missing)
            + "\n\nPopulate them and re-run.",
            title="Missing API keys",
            border_style="red",
            padding=(1, 2),
        )
    )
    raise typer.Exit(code=2)


def _build_config(checkpoint: bool) -> dict:
    """Assemble the run config. Mirrors what the interactive CLI builds.

    ``checkpoint`` defaults to True from the CLI so a crashed quorum run
    (frontier-model calls × deep-depth debate isn't cheap to redo from
    scratch) resumes from the last successful node on the next
    invocation. Pass ``--no-checkpoint`` to disable.
    """
    config = DEFAULT_CONFIG.copy()
    config["max_debate_rounds"] = _DEFAULT_RESEARCH_DEPTH
    config["max_risk_discuss_rounds"] = _DEFAULT_RESEARCH_DEPTH
    config["prompt_style"] = _DEFAULT_PROMPT_STYLE
    config["output_language"] = _DEFAULT_OUTPUT_LANGUAGE
    # ``thinking_policy`` is moot when every agent has its own LLM, but
    # set ``all_deep`` so any future agent missing from the routing map
    # still gets the deep fallback rather than a quick fallback.
    config["thinking_policy"] = "all_deep"
    config["checkpoint_enabled"] = checkpoint
    # Provider-specific scalar fields aren't used because per-agent kwargs
    # are baked into ``QUORUM_ROUTING`` directly.
    config["llm_provider"] = "openai"  # placeholder — graph won't read it in quorum mode
    config["deep_think_llm"] = "gpt-5.4"
    config["quick_think_llm"] = "deepseek-v4-flash"
    return config


def _print_run_header(ticker: str, date: str, checkpoint: bool) -> None:
    """One-screen summary of routing + pinned defaults before the run."""
    body = (
        f"[bold]Ticker[/bold]: {ticker}\n"
        f"[bold]Date[/bold]:   {date}\n"
        f"[bold]Analysts[/bold]: {', '.join(_DEFAULT_ANALYSTS)}\n"
        f"[bold]Depth[/bold]: deep ({_DEFAULT_RESEARCH_DEPTH} rounds bull/bear, "
        f"{_DEFAULT_RESEARCH_DEPTH} rounds risk panel)\n"
        f"[bold]Prompt style[/bold]: {_DEFAULT_PROMPT_STYLE}\n"
        f"[bold]Output language[/bold]: {_DEFAULT_OUTPUT_LANGUAGE}\n"
        f"[bold]Checkpoint resume[/bold]: {'on' if checkpoint else 'off'}\n\n"
        f"[bold]Per-agent routing[/bold]:\n{describe_routing()}"
    )
    console.print(
        Panel(
            body,
            title="TradingAgents Quorum",
            border_style="cyan",
            padding=(1, 2),
        )
    )


@app.command()
def run(
    ticker: str = typer.Argument(
        ...,
        help="Ticker symbol to analyze (e.g. AAPL, NVDA, 7203.T, 0700.HK).",
    ),
    date: Optional[str] = typer.Option(
        None,
        "--date",
        "-d",
        help="Analysis date in YYYY-MM-DD format. Defaults to today.",
    ),
    save: bool = typer.Option(
        True,
        "--save/--no-save",
        help="Persist a complete_report.md plus per-team subfolders to ./reports/<TICKER>_<TS>/.",
    ),
    save_dir: Optional[Path] = typer.Option(
        None,
        "--save-dir",
        help="Override the default save path (./reports/<TICKER>_<TS>/).",
    ),
    show_report: bool = typer.Option(
        True,
        "--show/--no-show",
        help="Echo the rendered report to the terminal after the run.",
    ),
    checkpoint: bool = typer.Option(
        True,
        "--checkpoint/--no-checkpoint",
        help=(
            "Save LangGraph state after each node so a crashed run "
            "resumes from the last successful step on the next "
            "invocation. ON by default in quorum mode (frontier-model "
            "calls × deep-depth debate is expensive to redo)."
        ),
    ),
    clear_checkpoints: bool = typer.Option(
        False,
        "--clear-checkpoints",
        help="Delete all saved checkpoints before running (force fresh start).",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Stream every LangGraph chunk's last message to stdout while running.",
    ),
) -> None:
    """Execute a quorum-routed analysis for ``TICKER``."""
    ticker = _validate_ticker(ticker)
    analysis_date = _validate_date(date)

    _abort_if_keys_missing()

    if clear_checkpoints:
        from tradingagents.graph.checkpointer import clear_all_checkpoints
        n = clear_all_checkpoints(DEFAULT_CONFIG["data_cache_dir"])
        console.print(f"[yellow]Cleared {n} checkpoint(s) before run.[/yellow]")

    _print_run_header(ticker, analysis_date, checkpoint)

    config = _build_config(checkpoint)

    # Stats callback is forwarded into every per-agent LLM client so a
    # single counter reports total LLM / tool / token usage across all
    # three vendors.
    stats_handler = StatsCallbackHandler()

    console.print("[dim]Building per-agent LLM clients...[/dim]")
    agent_llm_map = build_quorum_llm_map(callbacks=[stats_handler])
    reflector_llm = build_reflector_llm(callbacks=[stats_handler])

    console.print("[dim]Compiling LangGraph workflow...[/dim]")
    graph = TradingAgentsGraph(
        selected_analysts=_DEFAULT_ANALYSTS,
        config=config,
        debug=debug,
        callbacks=[stats_handler],
        agent_llm_map=agent_llm_map,
        reflector_llm=reflector_llm,
    )

    console.print(
        Rule(
            f"Running quorum analysis for [bold cyan]{ticker}[/bold cyan] "
            f"on [bold]{analysis_date}[/bold]",
            style="green",
        )
    )

    start = time.time()
    try:
        final_state, decision = graph.propagate(ticker, analysis_date)
    except Exception:
        logger.exception("Quorum analysis failed for %s on %s", ticker, analysis_date)
        raise

    elapsed = time.time() - start

    stats = stats_handler.get_stats()
    console.print(
        Panel(
            (
                f"[bold]Final rating[/bold]: {decision}\n"
                f"[bold]Elapsed[/bold]: {int(elapsed // 60):02d}:{int(elapsed % 60):02d}\n"
                f"[bold]LLM calls[/bold]: {stats.get('llm_calls', 0)}\n"
                f"[bold]Tool calls[/bold]: {stats.get('tool_calls', 0)}\n"
                f"[bold]Tokens[/bold]: "
                f"{stats.get('tokens_in', 0)}\u2191 / {stats.get('tokens_out', 0)}\u2193"
            ),
            title="Run summary",
            border_style="green",
            padding=(1, 2),
        )
    )

    if save:
        timestamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        target = save_dir or (Path.cwd() / "reports" / f"{ticker}_{timestamp}")
        try:
            report_file = save_report_to_disk(final_state, ticker, target)
            console.print(
                f"[green]Report saved:[/green] {report_file.resolve()}"
            )
        except Exception as exc:
            console.print(f"[red]Could not save report:[/red] {exc}")

    if show_report:
        display_complete_report(final_state)

    # Surface the rendered Portfolio Manager decision one last time so it
    # is the final thing in the user's terminal scrollback.
    console.print(Rule("Portfolio Manager Decision", style="bold green"))
    console.print(Markdown(final_state.get("final_trade_decision", decision)))


def main() -> None:
    """Console-script entry point.

    Wraps Typer's ``app()`` so a missing/invalid argument exits with a
    non-zero status and a readable message rather than a stack trace.
    """
    try:
        app()
    except typer.Exit:
        raise
    except KeyboardInterrupt:
        console.print("\n[red]Interrupted.[/red]")
        sys.exit(130)


if __name__ == "__main__":
    main()
