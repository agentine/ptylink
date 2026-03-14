"""Tests for _popen.py: PopenSpawn — non-PTY process interaction."""

from __future__ import annotations

from ptylink._popen import PopenSpawn
from ptylink._types import EOF_TYPE


class TestPopenSpawn:
    def test_basic_echo(self) -> None:
        """PopenSpawn should capture simple command output."""
        with PopenSpawn("echo hello") as child:
            child.expect("hello")
            assert "hello" in child.after

    def test_list_command(self) -> None:
        """PopenSpawn should accept list commands."""
        with PopenSpawn(["python3", "-c", "print(42)"]) as child:
            child.expect("42")
            assert "42" in child.after

    def test_expect_eof(self) -> None:
        """EOF sentinel should match when process exits."""
        with PopenSpawn("echo done") as child:
            child.expect("done")
            idx = child.expect([EOF_TYPE])
            assert idx == 0

    def test_sendline(self) -> None:
        """sendline should send input through stdin pipe."""
        with PopenSpawn("python3 -c \"x=input(); print('got:',x)\"") as child:
            child.sendline("hello")
            child.expect("got: hello")
            assert "got: hello" in child.after

    def test_sendeof(self) -> None:
        """sendeof should close stdin pipe."""
        with PopenSpawn("cat") as child:
            child.send("hello\n")
            child.sendeof()
            idx = child.expect([EOF_TYPE])
            assert idx == 0

    def test_wait_returns_exit_code(self) -> None:
        """wait() should return the exit code."""
        with PopenSpawn("true") as child:
            try:
                child.expect([EOF_TYPE])
            except Exception:
                pass
            code = child.wait()
            assert code == 0

    def test_wait_nonzero_exit(self) -> None:
        """wait() should return nonzero exit code."""
        with PopenSpawn("sh -c 'exit 2'") as child:
            try:
                child.expect([EOF_TYPE])
            except Exception:
                pass
            code = child.wait()
            assert code == 2

    def test_isalive(self) -> None:
        """isalive should reflect process state."""
        child = PopenSpawn("echo quick")
        try:
            child.expect([EOF_TYPE])
        except Exception:
            pass
        child.wait()
        assert not child.isalive()
        child.close()

    def test_context_manager(self) -> None:
        """Context manager should clean up."""
        with PopenSpawn("echo test") as child:
            child.expect("test")
        # After exit, process should be cleaned up.

    def test_multiline_output(self) -> None:
        """Should handle multiline output."""
        with PopenSpawn("printf 'line1\\nline2\\nline3'") as child:
            child.expect("line1")
            child.expect("line2")
            child.expect("line3")

    def test_with_env(self) -> None:
        """Should pass environment variables."""
        with PopenSpawn(
            "sh -c 'echo $TESTVAR'",
            env={"TESTVAR": "hello123", "PATH": "/usr/bin:/bin"},
        ) as child:
            child.expect("hello123")
