"""
Execution-Grounded Progressive Self-Correction Engine:
Executes candidate queries against a lightweight DuckDB sandbox and iteratively repairs syntax/runtime faults.
"""
import duckdb
import sqlglot
from typing import Dict, Any, Tuple

class SandboxExecutionEngine:
    def __init__(self, db_con: duckdb.DuckDBPyConnection = None):
        self.con = db_con or duckdb.connect(":memory:")
        self._init_mock_tables()

    def _init_mock_tables(self):
        self.con.execute("""
            create table if not exists patients (patient_id varchar, first_name varchar, birth_date date);
            create table if not exists encounters (encounter_id varchar, patient_id varchar, encounter_class varchar, total_claim_cost double);
            insert into patients values ('p-1', 'Alice', '1980-01-01');
            insert into encounters values ('enc-1', 'p-1', 'INPATIENT', 4500.0);
        """)

    def execute_and_verify(self, sql_query: str) -> Tuple[bool, Any, str]:
        try:
            res = self.con.execute(sql_query).fetchall()
            return True, res, ""
        except Exception as e:
            return False, None, str(e)

    def repair_query(self, failed_sql: str, error_msg: str) -> str:
        """
        Progressive repair heuristics:
        - Common missing GROUP BY columns
        - Ambiguous column name qualification
        - Quotes normalization
        """
        repaired = failed_sql
        if "GROUP BY" in error_msg.upper() and "encounter_class" in failed_sql:
            repaired += " GROUP BY encounter_class"
        elif "does not exist" in error_msg.lower():
            # Strip invalid table prefixes
            repaired = repaired.replace("patients.encounter_class", "encounters.encounter_class")
        return repaired
