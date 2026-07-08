# Contributing

## Setup

```bash
uv sync --group dev
pre-commit install
```

## Workflow

1. Create a branch off `main`.
2. Make your change, keeping it scoped to one concern.
3. Run checks locally before pushing:

   ```bash
   uv run ruff check .
   uv run black --check .
   uv run isort --check-only .
   uv run mypy src
   uv run pytest
   ```

4. Update `CHANGELOG.md` if the change is user-facing.
5. Open a PR using the provided template.

## Code style

- PEP 8, enforced by `ruff` + `black` + `isort`.
- Type hints on all new code; `mypy` must pass.
- No `print()` — use the module-level `logger = logging.getLogger(__name__)`.
- Never commit `.env`, `credentials.json`, or `token.json`.
