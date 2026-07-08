# Changelog

## [0.2.0] - 2026-07-08

### Changed
- Restructured into a `src/email_assistant/` layout: `config/`, `models/`, `services/`, `tools/`,
  `agents/`, `tasks/`, `cli/`. Entry point is now `email-assistant` (console script) or
  `python -m email_assistant.cli.main`.
- `GmailService`, `EmailCacheService`, `Settings` are now classes/dataclasses constructed in one
  composition root (`cli/main.py`) instead of relying on module-level globals.
- `GmailService` now falls back to a fresh OAuth flow on `RefreshError` instead of crashing.
- All modules use type hints, module-level loggers, and pathlib.
- Full lint/type/test tooling: ruff, black, isort, mypy, pytest, pre-commit.

### Added
- `tests/` — pytest suite for models, utils, cache service, Gmail service (mocked).
- GitHub Actions CI (ruff, black, mypy, pytest), issue templates, PR template.
- LICENSE (MIT), CONTRIBUTING.md, SECURITY.md, CODE_OF_CONDUCT.md.
- Log redaction filter (`utils/masking.py`) masking configured secrets in `logs/app.log`.

### Removed
- Dead code: `tools/groq_tool.py`, `tools/email_classifier.py`, `tools/response_generator.py` —
  a parallel Groq-based classification/reply path that was never imported by the actual
  pipeline (`main.py` always used the CrewAI `LLM` with `CUSTOM_LLM_*` config). Dropped the
  unused `groq` dependency and `GROQ_API_KEY` env var as a result.
- Ad-hoc scripts `test_agent.py`, `test_crew_llm.py` (hit live endpoints, not real tests) —
  replaced by the `tests/` pytest suite.

## [0.1.0] - 2026-07-08

### Added
- Gmail unread-email fetch, CrewAI reader/classifier/response-generator agents, sequential crew.
- SQLite classification cache (`database/cache.py`).
- File + console logging via `logger_config.py`.
- README, `.env.example`, gitignore hardening for secrets.

### Fixed
- `main.py`: report-writing block was mis-indented outside `main()`, causing `NameError` on every run (result/report code executed at import time before `result` existed). Moved inside `main()`.
- `main.py`: removed dead `from unittest import result` import and unused `output_file` variable.
- `.gitignore`: added `.env`, `credentials.json`, `token.json`, `logs/`, `database/*.db` — these held live secrets and were previously untracked but not ignored.
- Removed stray empty `tools/tools/` directory.
