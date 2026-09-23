# ADR 0005: DuckDB In-Memory Sandbox Isolation

## Status: Accepted
## Context
Evaluating queries on production databases incurs compute costs and data alteration risks.

## Decision
Execute test queries against an ephemeral DuckDB in-memory database.
