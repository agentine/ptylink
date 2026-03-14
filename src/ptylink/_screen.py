"""ANSI escape sequence handling."""

from __future__ import annotations

import re

# Matches all standard ANSI escape sequences:
# - CSI sequences: ESC [ ... final_byte
# - OSC sequences: ESC ] ... ST
# - Single-character controls: ESC + one byte
ANSI_ESCAPE_RE = re.compile(
    r"\x1b"
    r"(?:"
    r"\[[0-?]*[ -/]*[@-~]"  # CSI sequences
    r"|"
    r"\][\x20-\x7e]*(?:\x07|\x1b\\)"  # OSC sequences (BEL or ST terminated)
    r"|"
    r"[@-Z\\-_]"  # two-char ESC sequences (must be last — ] overlaps with OSC)
    r")"
)


def strip_ansi(text: str) -> str:
    """Remove all ANSI escape sequences from *text*."""
    return ANSI_ESCAPE_RE.sub("", text)


def has_ansi(text: str) -> bool:
    """Return True if *text* contains any ANSI escape sequences."""
    return bool(ANSI_ESCAPE_RE.search(text))
