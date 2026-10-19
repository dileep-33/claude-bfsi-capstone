# AI Banking Platform — Architecture

Layered integration developed inside Claude Code:

1. Repo instrumentation (CLAUDE.md) — authoritative development context.
2. MCP integration layer — customer-info, banking-api, github servers; every
   hop audited to audit_log/mcp_tool_calls.jsonl.
3. Claude Skills layer — six cached skills as the reasoning library.
4. Chatbot — guardrailed, streaming, fraud tool-use.
5. Fraud + KYC + Compliance pipeline — KYC -> AML -> Sanctions -> Approval.
6. Transaction processing — full audit trail; model routing Haiku/Sonnet/Opus.
7. Batch API fraud pipeline — synthetic transactions scored at the Haiku tier.
8. Hooks, slash commands, sub-agents — governance woven into the dev workflow.
9. CI/CD gate — headless Claude-as-Judge (score >= 4) blocks merge.
