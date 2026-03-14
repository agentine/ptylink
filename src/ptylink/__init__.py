"""ptylink — Modern process interaction library with PTY support."""

from __future__ import annotations

__version__ = "0.1.0"
__all__ = [
    "Spawn",
    "AsyncSpawn",
    "PopenSpawn",
    "SSHSession",
    "EOF",
    "EOFError",
    "TIMEOUT",
    "EOF_TYPE",
    "TIMEOUT_TYPE",
    "run",
    "spawn",
    "TetherError",
    "Timeout",
    "ExitStatus",
    "Pattern",
    "strip_ansi",
    "has_ansi",
]

# Foundational types
# Phase 3 — async, popen, ssh
from ptylink._async import AsyncSpawn
from ptylink._errors import EOF as EOFError
from ptylink._errors import ExitStatus, TetherError, Timeout
from ptylink._popen import PopenSpawn

# Phase 2 — run, screen, interact
from ptylink._run import run
from ptylink._screen import has_ansi, strip_ansi

# Phase 1 — Spawn
from ptylink._spawn import Spawn
from ptylink._ssh import SSHSession
from ptylink._types import EOF, EOF_TYPE, TIMEOUT, TIMEOUT_TYPE, Pattern


def spawn(
    command: str | list[str],
    *,
    timeout: float = 30,
    encoding: str = "utf-8",
) -> Spawn:
    """Spawn a process with PTY."""
    return Spawn(command, timeout=timeout, encoding=encoding)
