"""Exception hierarchy for ptylink."""

from __future__ import annotations


class TetherError(Exception):
    """Base exception for all ptylink errors."""


class Timeout(TetherError):
    """Raised when an expect operation times out."""

    __slots__ = ("pattern",)

    def __init__(self, pattern: str = "", msg: str | None = None) -> None:
        self.pattern = pattern
        super().__init__(msg or f"Timeout waiting for pattern: {pattern!r}")


class EOF(TetherError):
    """Raised when the process closes its output (end of file on PTY)."""

    __slots__ = ("before",)

    def __init__(self, before: str = "", msg: str | None = None) -> None:
        self.before = before
        super().__init__(msg or "End of file (EOF). Process has closed output.")


class ExitStatus(TetherError):
    """Raised when the process exits with a non-zero status."""

    __slots__ = ("status", "signal")

    def __init__(
        self,
        status: int,
        signal: int | None = None,
        msg: str | None = None,
    ) -> None:
        self.status = status
        self.signal = signal
        if msg is None:
            parts = [f"Process exited with status {status}"]
            if signal is not None:
                parts.append(f" (signal {signal})")
            msg = "".join(parts)
        super().__init__(msg)
