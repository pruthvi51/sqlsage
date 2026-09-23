# ADR 0004: Execution-Grounded Progressive Self-Correction

## Status: Accepted
## Context
Initial candidate queries occasionally miss subtle GROUP BY or JOIN qualifiers.

## Decision
Execute candidate SQL against a sandbox DuckDB database and apply progressive repair heuristics.
