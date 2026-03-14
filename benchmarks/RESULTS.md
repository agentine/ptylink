# Benchmark Results

**Environment:** Python 3.14, macOS Darwin 25.3.0
**Date:** 2026-03-13

## ptylink vs pexpect

| Operation | ptylink (µs/op) | pexpect (µs/op) | Ratio |
|-----------|---------------:|----------------:|------:|
| spawn+expect (echo) | 3002 | 285821 | 95.21x |
| spawn+expect (python) | 84312 | 307303 | 3.64x |
| run (echo) | 3352 | 163946 | 48.92x |

ptylink is **3.6×–95.2×** faster than pexpect across all operations.
