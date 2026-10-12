# SQLSage Operational Runbook & Query Triage Manual

This document details operational triage protocols, schema linking synchronization procedures, and error recovery playbooks for the SQLSage Natural Language to SQL translation engine.

---

## Playbook 1: Schema Ingestion & MinHash LSH Entity Index Synchronization

### Severity: High (Entity Linking Degraded)
**Symptom:** Clinicians input domain terminology (e.g., *"hypertension"*, *"HbA1c"*, *"capitated spend"*), but MinHash LSH fails to resolve target tables, defaulting to fallback entities.

### Triage & Resolution:
1. **Inspect Token Dictionary:**
   Verify whether canonical terminology and clinical aliases are registered in `MinHashLSHIndex`:
   ```python
   from sqlsage.schema_graph.minhash_lsh import MinHashLSHIndex
   lsh = MinHashLSHIndex()
   # Verify entity matches
   matches = lsh.match_entity("Find patients with severe hypertension")
   ```
2. **Synchronize New Clinical Aliases:**
   When adding new clinical concepts or warehouse tables, update the alias dictionary in `src/sqlsage/cli.py` and `ui/app.py`:
   ```python
   lsh.add_value("conditions", ["hypertension", "htn", "essential hypertension", "i10"])
   ```
3. **Verify Recall:**
   Run entity linking verification:
   ```bash
   pytest -v tests/test_schema_graph.py
   ```

---

## Playbook 2: Ambiguous NL Query Triage & Disambiguation Protocol

### Severity: Medium (Semantic Ambiguity)
**Symptom:** Query contains multi-meaning terms (e.g., *"cost"* which could refer to `encounters.total_claim_cost` or `claims.total_billed`).

### Protocol:
1. **Check Steiner Subgraph Path:**
   Run the CLI graph tool to evaluate candidate join subgraphs:
   ```bash
   sqlsage graph --tables encounters,claims
   ```
2. **Examine Generated SQL:**
   Test translation directly via CLI:
   ```bash
   sqlsage translate "What was the total cost for patient p-1?"
   ```
3. **Disambiguation Guidance:**
   If the user intent targets billed claims rather than encounter claims, guide the user to specify *"billed amount"* or *"claim reimbursement"*.

---

## Playbook 3: AST Grammar Mask Violation Triage & Schema Drift

### Severity: High (Translation Blocked)
**Symptom:** `GrammarMaskValidator` reports `Hallucinated Table` or `Hallucinated Column`.

### Triage Steps:
1. **Identify Hallucinated Token:**
   Check the validation errors emitted by `GrammarMaskValidator`:
   ```python
   from sqlsage.constrained_decoding.grammar_mask import GrammarMaskValidator
   valid, errors = validator.validate_ast(sql_query)
   ```
2. **Schema Drift Detection:**
   Determine whether the upstream database added new columns that are not yet reflected in `valid_schema`.
3. **Update Grammar Mask Catalog:**
   Update the schema dictionary in `src/sqlsage/constrained_decoding/` to include new attributes, then re-run test suite:
   ```bash
   pytest -v tests/test_constrained_decoding.py
   ```

---

## Playbook 4: Sandboxed DuckDB Memory Allocation & Isolation Tuning

### Severity: Medium (Sandbox Performance)
**Symptom:** Complex analytical queries (window functions, multi-way joins) encounter memory timeouts in the sandbox.

### Configuration Protocol:
1. **Inspect Sandbox Connections:**
   In `src/sqlsage/agent/self_correction.py`, DuckDB operates in `:memory:` mode with sub-2ms query times.
2. **Apply Resource Limits:**
   In production multi-tenant deployments, enforce execution thread and memory caps:
   ```sql
   SET threads TO 2;
   SET max_memory = '512MB';
   ```
3. **Test Sandbox Execution:**
   ```bash
   pytest -v tests/test_self_correction.py
   ```

---

## Playbook 5: Evaluation Dataset Drift Monitoring & Retesting

### Severity: Low (Periodic Maintenance)
**Symptom:** Upstream lakehouse evolves with new analytical data marts (e.g. chronic disease cohorts).

### Protocol:
1. **Audit CareLake-QA Benchmark Dataset:**
   Verify `data/carelake_qa_dataset.json` contains 150 balanced queries across Easy (50), Medium (50), and Hard (50) tiers.
2. **Run Full Benchmark Suite:**
   ```bash
   make bench
   ```
3. **Verify Key Performance Invariants:**
   - Execution Accuracy: $\ge 84.0\%$
   - Syntax Validity: $100.0\%$
   - Hallucination Rate: $0.0\%$
   - Autonomous Self-Correction Repair: $\ge 40.0\%$

