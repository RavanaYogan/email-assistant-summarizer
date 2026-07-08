# Security Policy

## Reporting a Vulnerability

If you find a security issue (leaked credential handling, OAuth flow flaw, injection risk, etc.),
please open a private report via GitHub's "Report a vulnerability" feature on this repo's
Security tab, rather than a public issue. Include:

- A description of the issue and its impact
- Steps to reproduce
- Affected version/commit

## Secrets

This project reads secrets from environment variables and local files that must never be
committed:

- `.env` (LLM API key, endpoint)
- `credentials.json` (Google OAuth client)
- `token.json` (Google OAuth user token)

All three are gitignored. Logs are passed through a redaction filter
(`email_assistant.utils.masking.SensitiveDataFilter`) that masks configured secret values before
they reach `logs/app.log` or stdout — but avoid logging raw secrets anywhere in new code regardless.
