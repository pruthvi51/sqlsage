# ADR 0003: AST Grammar Masking for Zero Hallucinations

## Status: Accepted
## Context
LLMs hallucinate non-existent table and column names.

## Decision
Enforce schema-guided constrained decoding via SQLGlot AST validation.
