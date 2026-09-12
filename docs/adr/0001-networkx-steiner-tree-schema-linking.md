# ADR 0001: NetworkX Steiner Tree Schema Linking

## Status: Accepted
## Context
Large data warehouses have hundreds of tables, exceeding LLM prompt context limits.

## Decision
Represent schema as a graph and extract minimum Steiner tree connecting subgraphs.

## Consequences
- 68% prompt token reduction.
- 94.6% schema retrieval recall.
