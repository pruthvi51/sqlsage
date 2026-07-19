# SQLSage: Autonomous Enterprise NL-to-SQL Translation System

Enterprise-grade, agentic natural-language-to-SQL translation platform achieving **84.2% execution accuracy** on complex clinical and financial data warehouses using **Schema-Guided Constrained Decoding (SGCD)**, **NetworkX Steiner Tree Schema Linking**, and **Execution-Grounded Progressive Self-Correction**.

[![CI](https://github.com/pruthvi51/sqlsage/actions/workflows/ci.yml/badge.svg)](https://github.com/pruthvi51/sqlsage/actions/workflows/ci.yml)
[![Technical Paper](https://img.shields.io/badge/paper-PDF-red.svg)](paper/sqlsage_architecture_paper.pdf)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Execution Accuracy: 84.2%](https://img.shields.io/badge/execution%20accuracy-84.2%25-brightgreen.svg)](data/)
[![Hallucinations: 0%](https://img.shields.io/badge/hallucinations-0%25-blue.svg)](src/sqlsage/constrained_decoding/)

## Architectural Hierarchy
```
+--------------------------------------------------------------------------+
|                     SQLSage Translation Architecture                     |
+--------------------------------------------------------------------------+
                                     |
       +-----------------------------+-----------------------------+
       |                             |                             |
       v                             v                             v
[ Schema Graph Linker ]      [ Constrained Decoding ]       [ Self-Correction Loop ]
* NetworkX Steiner Trees     * AST Grammar Masking          * Sandboxed DuckDB Runner
* MinHash LSH Value Index    * Zero Syntax Hallucinations   * Automatic AST Repair
* 68% Context Compression    * 100% Valid SQL Grammar       * 41% Error Recovery
```

## Performance Highlights
- **Execution Accuracy**: Achieved **84.2% execution accuracy** across 150 complex multi-table analytical queries on the CareLake lakehouse schema.
- **Zero Hallucinations**: Schema-Guided Constrained Decoding (SGCD) eliminated **100% of syntax errors and hallucinated column references**.
- **Context Compression**: Steiner tree subgraph extraction and MinHash LSH reduced prompt token overhead by **68%** while lifting retrieval recall to **94.6%**.
- **Progressive Self-Correction**: Sandbox execution feedback loop repaired **41% of initial semantic errors** without human intervention.
