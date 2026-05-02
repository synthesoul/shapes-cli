# AGENTS.md

## Project Overview

`shapes-cli` is a single-file Python command-line chat client for the Shapes API.
It prompts for an API key and model name, opens a chat session, supports basic
session commands, and persists conversation logs under `chatlogs/`.

## Key Files

- `shape.py` - interactive CLI entry point and main application logic.
- `scripts/doctor.py` - repository health check and environment report.
- `README.md` - quickstart and repository notes.
- `.gitignore` - local cache, log, and virtual environment exclusions.

## Setup

- Use Python 3 on a local development machine.
- Install the runtime dependency used by the CLI:
  - `pip install openai`
- If you want audio playback for MP3 responses, install `mpg123`.

## Run Commands

- Start the CLI: `python shape.py`
- Run the repo doctor: `python scripts/doctor.py`
- Syntax check: `python -m py_compile shape.py scripts/doctor.py`

## Test, Lint, Build

- Test command: not detected.
- Lint command: not detected.
- Build command: not detected.
- This repo currently appears to be a small script project rather than a
  packaged application.

## Coding Conventions

- Keep the code Pythonic and direct.
- Preserve the current interactive console flow unless a change is explicitly
  requested.
- Prefer small, localized edits over broad refactors.
- Match the existing style of standard-library imports, simple helper functions,
  and straightforward control flow.

## Editing Safety Rules

- Do not rewrite unrelated behavior while adding docs or tooling.
- Avoid introducing heavyweight dependencies.
- Do not delete user chat logs or generated files.
- Keep any new tooling optional and non-invasive.
- If you need to change runtime behavior, confirm the scope first.

## Instructions for Future Codex Agents

- Read `shape.py` first; it is the whole app.
- Check `scripts/doctor.py` before guessing at setup or commands.
- If a dependency or command is not present in the repo, document it as
  "not detected" rather than inferring too much.
- Prefer lightweight repository onboarding improvements over feature work when
  the repo has no baseline documentation.