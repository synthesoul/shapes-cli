# shapes-cli

`shapes-cli` is a small Python command-line client for the Shapes API.
It opens an interactive chat session, supports a few session commands, and
stores conversation history in local `chatlogs/` folders.

## Development Quickstart

1. Install Python 3.
2. Install the runtime dependency:
   - `pip install openai`
3. Run the health check:
   - `python scripts/doctor.py`
4. Start the CLI:
   - `python shape.py`

## Repository Notes

- Main entry point: `shape.py`
- Agent guidance: [`AGENTS.md`](./AGENTS.md)
- Repository health check: [`scripts/doctor.py`](./scripts/doctor.py)

## Testing

No automated test suite was detected in this repository.
The recommended lightweight verification is:

- `python scripts/doctor.py`
- `python -m py_compile shape.py scripts/doctor.py`

## Runtime Notes

- The CLI prompts for a Shapes API key at startup.
- The optional audio playback path uses `mpg123` if it is installed.
- Chat logs are written under `chatlogs/<model-name>/`.