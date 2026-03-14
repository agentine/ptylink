"""pexpect compatibility shim.

Use ``import ptylink._compat as pexpect`` or
``import ptylink.compat as pexpect`` for a drop-in replacement.

Example::

    import ptylink.compat as pexpect
    child = pexpect.spawn("echo hello")
    child.expect("hello")
"""

from __future__ import annotations

# EOF / TIMEOUT — pexpect exports these as exception classes that also serve
# as sentinels in expect() pattern lists.  Mapping to ptylink's exception
# classes lets ``except pexpect.EOF:`` work correctly.
from ptylink._errors import EOF as EOF  # noqa: PLC0414

# Explicit exception aliases (pexpect compat names).
from ptylink._errors import EOF as ExceptionEOF  # noqa: PLC0414
from ptylink._errors import TetherError as ExceptionPexpect  # noqa: PLC0414
from ptylink._errors import Timeout as ExceptionTimeout  # noqa: PLC0414
from ptylink._errors import Timeout as TIMEOUT  # noqa: PLC0414

# High-level run — pexpect.run ↔ ptylink.run
from ptylink._run import run
from ptylink._spawn import Spawn

# Core classes — pexpect.spawn ↔ ptylink.Spawn
from ptylink._spawn import Spawn as spawn  # noqa: N811 (pexpect names are lowercase)

# SSH — pexpect.pxssh ↔ ptylink.SSHSession
from ptylink._ssh import SSHSession as pxssh

__all__ = [
    "spawn",
    "Spawn",
    "run",
    "EOF",
    "TIMEOUT",
    "ExceptionPexpect",
    "ExceptionEOF",
    "ExceptionTimeout",
    "pxssh",
]
