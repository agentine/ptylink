"""Tests for _run.py: high-level run() function."""

from __future__ import annotations

from ptylink._run import run


class TestRun:
    def test_basic_echo(self) -> None:
        result = run("echo hello")
        assert "hello" in result

    def test_withexitstatus_success(self) -> None:
        output, status = run("echo hi", withexitstatus=True)  # type: ignore[misc]
        assert "hi" in output
        assert status == 0

    def test_withexitstatus_failure(self) -> None:
        output, status = run("sh -c 'exit 2'", withexitstatus=True)  # type: ignore[misc]
        assert status == 2

    def test_without_exitstatus(self) -> None:
        result = run("echo test")
        assert isinstance(result, str)
        assert "test" in result

    def test_multiline_output(self) -> None:
        result = run("printf 'line1\\nline2\\nline3'")
        assert "line1" in result
        assert "line2" in result
        assert "line3" in result

    def test_events(self) -> None:
        """Test event-based interaction."""
        result = run(
            "sh -c 'echo Question?; read ans; echo Answer: $ans'",
            events={"Question?": "yes\n"},
        )
        assert "Answer: yes" in result

    def test_run_empty_command(self) -> None:
        result = run("true")
        assert isinstance(result, str)

    def test_run_with_env(self) -> None:
        result = run("sh -c 'echo $TESTVAR'", env={"TESTVAR": "hello123", "PATH": "/usr/bin:/bin"})
        assert "hello123" in result
