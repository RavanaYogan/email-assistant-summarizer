# Changelog

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
