#!/usr/bin/env python3
"""Lightweight repository health check for shapes-cli."""

from __future__ import annotations

import importlib.util
import os
import platform
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def status_line(label: str, message: str) -> None:
    print(f"[{label}] {message}")


def check_python() -> list[str]:
    warnings: list[str] = []
    version = sys.version_info
    status_line("OK", f"Python {platform.python_version()} ({sys.executable})")
    if version < (3, 10):
        warnings.append("Python 3.10+ is recommended for a modern CLI workflow.")
    return warnings


def check_venv() -> list[str]:
    if os.environ.get("VIRTUAL_ENV") or sys.prefix != getattr(sys, "base_prefix", sys.prefix):
        status_line("OK", "Virtual environment appears active.")
        return []
    status_line("WARN", "No active virtual environment detected.")
    return ["Activate a virtual environment before installing dependencies."]


def check_dependency_files() -> list[str]:
    candidates = [
        "requirements.txt",
        "pyproject.toml",
        "Pipfile",
        "setup.py",
    ]
    found = [name for name in candidates if (ROOT / name).exists()]
    if found:
        status_line("OK", f"Dependency files found: {', '.join(found)}")
        return []
    status_line("WARN", "No dependency file detected.")
    return ["Add a dependency file if the project grows beyond a single script."]


def check_runtime_dependency() -> list[str]:
    if importlib.util.find_spec("openai") is not None:
        status_line("OK", "Python package 'openai' is importable.")
        return []
    status_line("WARN", "Python package 'openai' is not importable.")
    return ["Install the runtime dependency with: pip install openai"]


def check_entry_files() -> list[str]:
    warnings: list[str] = []
    entry_files = ["shape.py"]
    missing = [name for name in entry_files if not (ROOT / name).exists()]
    if missing:
        status_line("WARN", f"Missing expected entry files: {', '.join(missing)}")
        warnings.append("The primary CLI entry file is missing.")
    else:
        status_line("OK", f"Entry file found: {', '.join(entry_files)}")

    if (ROOT / "chatlogs").exists():
        status_line("OK", "chatlogs/ directory exists.")
    else:
        status_line("INFO", "chatlogs/ directory does not exist yet; it is created at runtime.")
    return warnings


def check_tests() -> list[str]:
    test_paths = []
    for pattern in ("test_*.py", "*_test.py"):
        test_paths.extend(ROOT.rglob(pattern))
    if test_paths:
        status_line("OK", f"Detected test files: {len(test_paths)}")
        return []
    status_line("WARN", "No test files detected.")
    return ["No automated tests were found."]


def report_inferred_commands() -> None:
    print("\nInferred commands:")
    print("- Run the CLI: python shape.py")
    print("- Syntax check: python -m py_compile shape.py scripts/doctor.py")
    print("- Repo doctor: python scripts/doctor.py")
    print("- Test command: not detected")
    print("- Lint command: not detected")
    print("- Build command: not detected")


def main() -> int:
    print("shapes-cli repository doctor\n")
    warnings: list[str] = []
    warnings.extend(check_python())
    warnings.extend(check_venv())
    warnings.extend(check_dependency_files())
    warnings.extend(check_runtime_dependency())
    warnings.extend(check_entry_files())
    warnings.extend(check_tests())
    report_inferred_commands()

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("\nNo warnings detected.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())