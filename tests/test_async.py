"""Tests for _async.py: AsyncSpawn with native async/await."""

from __future__ import annotations

import asyncio

import pytest

from ptylink._async import AsyncSpawn
from ptylink._types import EOF_TYPE


class TestAsyncSpawn:
    def test_basic_echo(self) -> None:
        """AsyncSpawn should be able to run a simple command."""

        async def _run() -> str:
            async with AsyncSpawn("echo hello") as child:
                await child.expect("hello")
                return child.before + child.after

        result = asyncio.run(_run())
        assert "hello" in result

    def test_async_context_manager(self) -> None:
        """async with should work for cleanup."""

        async def _run() -> bool:
            async with AsyncSpawn("echo test") as child:
                await child.expect("test")
            return True

        assert asyncio.run(_run())

    def test_sendline_and_expect(self) -> None:
        """sendline/expect round-trip through a PTY."""

        async def _run() -> str:
            async with AsyncSpawn("python3 -c \"x=input(); print('got:',x)\"") as child:
                await child.sendline("hello")
                await child.expect("got: hello")
                return child.after

        result = asyncio.run(_run())
        assert "got: hello" in result

    def test_before_no_echo_leak(self) -> None:
        """before should not contain leaked sendline input."""

        async def _run() -> str:
            async with AsyncSpawn("python3") as child:
                await child.expect(">>> ")
                await child.sendline("print(42)")
                await child.expect("42")
                return child.before

        before = asyncio.run(_run())
        # before should not contain the sent "print(42)" text
        assert "print(42)" not in before

    def test_expect_eof(self) -> None:
        """EOF sentinel should match when process exits."""

        async def _run() -> int:
            async with AsyncSpawn("echo done") as child:
                await child.expect("done")
                # Give the process a moment to fully exit.
                await asyncio.sleep(0.3)
                idx = await child.expect([EOF_TYPE], timeout=5)
                return idx

        assert asyncio.run(_run()) == 0

    def test_isalive(self) -> None:
        """isalive should reflect process state."""

        async def _run() -> tuple[bool, bool]:
            child = AsyncSpawn("sleep 0.1")
            alive_before = await child.isalive()
            await asyncio.sleep(0.5)
            # Drain to detect EOF
            try:
                await child.expect([EOF_TYPE], timeout=2)
            except Exception:
                pass
            alive_after = await child.isalive()
            await child.close()
            return alive_before, alive_after

        before, after = asyncio.run(_run())
        assert before is True
        assert after is False

    def test_sendcontrol(self) -> None:
        """sendcontrol should send control characters."""

        async def _run() -> bool:
            async with AsyncSpawn("cat") as child:
                await asyncio.sleep(0.2)
                await child.sendcontrol("c")
                # Wait for process to die.
                for _ in range(50):
                    if not await child.isalive():
                        return True
                    await asyncio.sleep(0.1)
                return not await child.isalive()

        assert asyncio.run(_run())

    def test_timeout(self) -> None:
        """Timeout should raise ptylink.Timeout."""
        from ptylink._errors import Timeout

        async def _run() -> None:
            async with AsyncSpawn("sleep 10") as child:
                await child.expect("will_never_match", timeout=0.5)

        with pytest.raises(Timeout):
            asyncio.run(_run())

    def test_no_deprecation_warnings(self) -> None:
        """No DeprecationWarning from asyncio usage."""
        import warnings

        async def _run() -> None:
            with warnings.catch_warnings():
                warnings.simplefilter("error", DeprecationWarning)
                async with AsyncSpawn("echo ok") as child:
                    await child.expect("ok")

        asyncio.run(_run())
