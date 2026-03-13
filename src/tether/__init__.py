"""tether — Modern process interaction library with PTY support."""

from __future__ import annotations

__version__ = "0.1.0"
__all__ = [
    "Spawn",
    "AsyncSpawn",
    "PopenSpawn",
    "SSHSession",
    "EOF",
    "TIMEOUT",
    "EOF_TYPE",
    "TIMEOUT_TYPE",
    "run",
    "spawn",
    "TetherError",
    "Timeout",
    "ExitStatus",
    "Pattern",
]

# Foundational types
from tether._errors import ExitStatus, TetherError, Timeout
from tether._types import EOF, TIMEOUT, EOF_TYPE, TIMEOUT_TYPE, Pattern

# Phase 1 — Spawn
from tether._spawn import Spawn


# Stubs — replaced as phases are implemented.

class AsyncSpawn:
    """Async process interaction via PTY. Stub — see Phase 3."""


class PopenSpawn:
    """Non-PTY process interaction via pipes. Stub — see Phase 3."""


class SSHSession:
    """SSH session helper. Stub — see Phase 3."""


def run(command: str, *, timeout: float = 30) -> str:
    """Run a command and return its output. Stub — see Phase 2."""
    raise NotImplementedError("tether.run() not yet implemented")


def spawn(
    command: str | list[str],
    *,
    timeout: float = 30,
    encoding: str = "utf-8",
) -> Spawn:
    """Spawn a process with PTY."""
    return Spawn(command, timeout=timeout, encoding=encoding)
