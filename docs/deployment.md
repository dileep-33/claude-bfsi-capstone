# Deployment Guide

- Python 3.10+; `pip install anthropic python-dotenv mcp bandit pytest`.
- Secrets via environment (.env): OPENROUTER_API_KEY, GITHUB_TOKEN, model slugs.
- Register MCP servers via .claude/mcp.json; validate with the Phase 2 trace.
- Enable hooks in .claude/settings.json (PreToolUse audit, PostToolUse bandit).
- Gate merges on .github/workflows/ci_gate.yml: pytest, bandit, Claude-as-Judge.
- Audit logs under audit_log/ are the compliance system of record.
